import os,re
import subprocess
from memory import Memory
from config import client,LLM_MODEL



def list_files(path:str)->str:
    files=os.listdir(path)
    return "\n".join(files)

def read_file(path:str)->str:
    with open(path,"r",encoding="utf-8") as f:
        return f.read()
    
def write_file(path:str,content:str)->str:
    with open(path,"w",encoding="utf-8") as f:
        f.write(content)
    content = read_file(path)
    category, file_path, summary = summarize_file(
        path,
        content
    )

    memory.upsert_file_summary(
        file_path,
        summary
    )

    return "Modified"
def run_python(path:str)->str:
    result=subprocess.run(
        ["python",path],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode==0:
        return result.stdout

def search_files(keyword:str)->str:
    matches=[]
    for root,dirs,files in os.walk("."):
        for file in files:
            if keyword.lower() in file.lower():
                matches.append(
                    os.path.join(root,file)
                )
    if not matches:
        return "No matches"
    return "\n".join(matches)

def search_code(keyword:str)->str:
    matches=[]
    for root,dirs,files in os.walk("."):
        for file in files:
            if not file.endswith(".py"):
                continue
            path=os.path.join(root,file)
            with open(path,"r",encoding="utf-8") as f:
                for line_num,line in enumerate(f,start=1):
                    if keyword.lower() in line.lower():
                        matches.append(
                            f"{path}:{line_num}:{line.strip()}"
                        )

    if not matches:
        return "No matches"            
                
    return "\n".join(matches[:50])

memory=Memory()        
def show_memory() -> str:
    return memory.get_recent(20)


def search_memory(query:str)->str:
    return memory.search(query)

def call_llm(messages:list)->str:
    try:
        response=client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n[ERROR]:{e}")
        return ""

def summarize_file(path,content):
    prompt = f"""
Summarize the following file in ONE sentence.

Focus on:
- purpose of the file
- major responsibility

File: {path}

Content:
{content[:3000]}
"""
    messages=[
        {"role":"user","content":prompt}
    ]

    summary=call_llm(messages)
    return (
        "file_summary",
        path,
        summary
    )
    


def summarize_memory(tool_name, args, tool_result):
    

    if tool_name == "calculator":
        return (
            "calculation",
            f"{args[0]}" ,
            f"{tool_result}"
        )

    elif tool_name == "write_file":
        return (
            "file_write",
            f"Modified file {args[0]}",
            tool_result
        )

    elif tool_name == "run_python":
        return (
            "execution",
            f"Executed {args[0]}",
            tool_result
        )

    elif tool_name == "search_files":
        return (
            "file_search",
            f"Searched files for '{args[0]}'",
            tool_result
        )

    elif tool_name == "search_code":
        return (
            "code_search",
            f"Searched code for '{args[0]}'",
            tool_result
        )

    elif tool_name == "list_files":
        return (
            "directory_scan",
            f"Scanned directory {args[0]}",
            tool_result
        )

    elif tool_name == "read_file":
        if memory.has_file_summary(args[0]):
            return None

        category, summary, result = summarize_file(
            args[0],
            tool_result
        )

        return (
            category,
            summary,
            result
        )
    elif tool_name == "search_memory":

        return (
            "memory_search",
            f"Searched memory for '{args[0]}'",
            tool_result
        )
    elif tool_name == "edit_file":

        return (
            "file_edit",
            f"Edited file {args[0]}",
            f"Modified"
        )
    return (
    "general",
    f"Used tool {tool_name}",
    f"Result: {tool_result}"
    )


def build_project_knowledge():
    files=[]
    for file in os.listdir("."):
        if file.endswith(".py") or file.endswith(".json"):
            files.append(file)
    for file in files:
        if memory.has_file_summary(file):
            continue
        content=read_file(file)
        category, summary, result = summarize_file(
            file,
            content
        )

        memory.upsert_file_summary(
                summary,
                result
            )

    return f"Indexed {len(files)} files",print("MEMORIES:", len(memory.notes))

def parse_tool_call(text: str):

    # Handle write_file separately (needs multiline content)
    match = re.search(
        r"TOOL_CALL:\s*write_file\s*\|\s*(.+?)\s*\|\s*(.*)",
        text,
        re.DOTALL
    )

    if match:
        return "write_file", [
            match.group(1).strip(),
            match.group(2)
        ]

    # For every other tool, only parse the first line
    first_line = text.splitlines()[0]

    match = re.search(
        r"TOOL_CALL:\s*(\w+)\s*\|\s*(.+)",
        first_line
    )

    if match:
        tool_name = match.group(1).strip()

        args = [
            arg.strip()
            for arg in match.group(2).split("|")
        ]

        return tool_name, args

    match = re.search(
        r"TOOL_CALL:\s*(\w+)",
        first_line
    )

    if match:
        return match.group(1).strip(), []

    return None, []

def get_file_context(path):
    summary=memory.get_file_summary(path)
    if summary:
        return(
            f"[MEMORY]\n"
            f"{summary}"
        )
    content=read_file(path)
    category,summary_name,summary_text=summarize_file(
        path,
        content
    )

    memory.upsert_file_summary(
        summary_name,
        summary_text
    )

    return (
        f"[NEW SUMMARY]\n"
        f"{summary_text}"
        )

def edit_file(path:str,old_text:str,new_text:str)->str:
    content=read_file(path)
    if old_text not in content:
        return "Text not found"
    updated_content=content.replace(
        old_text,new_text,1
    )

    write_file(
        path,
        updated_content
    )
    return "File edited successfully"

def insert_after(path:str,marker:str,new_content:str)->str:
    content=read_file(path)
    position=content.find(marker)
    if position==-1:
        return f"""
            Marker not found.

            Closest matches:
            {content[-500:]}
            """
    
    insert_position=position+len(marker)
    updated_content=(
        +"\n\n"
        +new_content
        +content[insert_position:]
    )

    write_file(
        path,updated_content
    )

    return "Content Inserted"
