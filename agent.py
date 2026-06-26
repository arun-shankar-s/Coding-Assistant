from tools import list_files,read_file,write_file,run_python,search_files,search_code,memory,show_memory,search_memory,build_project_knowledge,call_llm,summarize_memory,parse_tool_call,get_file_context,edit_file


def calculator(expression:str)->str:
    allowed=set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "Error:Invalid Characters"
    try:
        result=eval(expression,{"__builtins__":{}},{})
        return str(result)
    except Exception as e:
        return f"Error:{e}"
    

TOOLS={
    "calculator":calculator,
    "list_files":list_files,
    "read_file":read_file,
    "write_file":write_file,
    "run_python":run_python,
    "search_files": search_files,
    "search_code": search_code,
    "show_memory":show_memory,
    "search_memory":search_memory,
    "build_project_knowledge":build_project_knowledge,
    "get_file_context":get_file_context,
    "edit_file":edit_file,
}

TOOLS_DESCRIPTION="""
Available Tools

1. calculator
   Description:
   Evaluates mathematical expressions and returns the result.

   Usage:
   TOOL_CALL: calculator | <expression>

2. list_files
   Description:
   Lists files and folders in a directory.

   Usage:
   TOOL_CALL: list_files | <path>

3. read_file
   Description:
   Reads the contents of a file.

   Usage:
   TOOL_CALL: read_file | <path>

4. write_file

Description:
Writes content to a file.

Usage:
TOOL_CALL: write_file | <path> | <content>

5. run_python

Description:
Executes a Python file and returns its output.

Usage:
TOOL_CALL: run_python | <path>

6. search_files

Description:
Searches filenames for a keyword.

Usage:
TOOL_CALL: search_files | <keyword>

7. search_code

Description:
Searches source code for a keyword.

Usage:
TOOL_CALL: search_code | <keyword>

8. search_memory

Description:
Searches stored memory entries.

Usage:
TOOL_CALL: search_memory | <keyword>

8. build_project_knowledge

Description:
Analyzes the project and stores summaries of files into memory.

Usage:
TOOL_CALL: build_project_knowledge

9. get_file_context

Description:
Returns a file summary from memory.
If no summary exists, reads the file,
creates a summary, stores it in memory,
and returns the summary.

Usage:
TOOL_CALL: get_file_context | <path>

10.edit_file

Description:
Replaces a specific piece of text in a file.

Usage:
TOOL_CALL: edit_file | <path> | <old_text> | <new_text>

"""    

SYSTEM_PROMPT=f"""
You are an AI agent.
Available Tools:
{TOOLS_DESCRIPTION}

Rules:

- If you need a tool, respond ONLY with:
  TOOL_CALL: <tool_name> | <input>
- After receiving a TOOL_RESULT, continue reasoning.
- When the task is complete, respond ONLY with:
  FINAL ANSWER: <answer>
- Do not invent tool results.
- To inspect folders use list_files.
- To inspect file contents use read_file.
- For arithmetic use calculator.
- To search previous memories use search_memory.
- You MUST use search_memory when answering questions about memory.
- To create or modify files, use write_file.
- To execute Python scripts use run_python.
- To locate relevant files, use search_files.
- To find code containing a keyword, use search_code.
- When trying to understand what a file does,
use get_file_context.

Only use read_file when:
- exact code is required
- implementation details are required
- code modification is required
-Every completed task MUST end with:
FINAL ANSWER: <answer>
Never answer directly.
Never omit FINAL ANSWER.
-Never output TOOL_CALL and FINAL ANSWER in the same response.

If a tool is needed:
Output only the TOOL_CALL.

After receiving TOOL_RESULT:
Output FINAL ANSWER.
"""


def run_agent(user_query: str, max_steps: int = 6):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\nMEMORY:\n" + memory.get_recent(10)},
        {"role": "user", "content": user_query}
    ]

    for step in range(1, max_steps + 1):
        print(f"\n[Step {step}] Thinking...")
        reply = call_llm(messages)
        print(f"\nAGENT:\n{reply}")

        if reply.startswith("FINAL ANSWER:"):
            final = reply.replace("FINAL ANSWER:", "").strip()
            print(f"\nFINAL ANSWER: {final}")
            return final
            
        tool_name, args = parse_tool_call(reply)

        if tool_name:
            if tool_name not in TOOLS:
                print(f"Unknown tool: {tool_name}")
                return None
            if tool_name == "build_project_knowledge":

                tool_result = TOOLS[tool_name]()

                print(f"\n[Tool] {tool_name}")
                print(f"[Tool Result] {tool_result}")

                messages.append({
                    "role": "assistant",
                    "content": reply
                })

                messages.append({
                    "role": "user",
                    "content": f"TOOL_RESULT: {tool_result}"
                })

                continue

            tool_result = TOOLS[tool_name](*args)
            if tool_name not in ["search_memory", "show_memory","get_file_context"]:
                
                memory_entry  = summarize_memory(
                    tool_name,
                    args,
                    tool_result
                )
                if memory_entry:
                    category, summary, result = memory_entry
                    if category == "file_summary":
                        memory.upsert_file_summary(
                            summary,
                            result
                        )

                    else:
                        memory.add(
                            category,
                            summary,
                            result
                        )
            
            print(f"\n[Tool] {tool_name}({args})")
            print(f"[Tool Result] {tool_result}")

            messages.append({
                "role": "assistant",
                "content": reply
            })

            messages.append({
                "role": "user",
                "content": f"TOOL_RESULT: {tool_result}"
            })

            continue

        print(f"\nFINAL ANSWER: {reply}")
        return reply

    print("Max steps reached.")
    return None

if __name__=="__main__":
    while True:
        user_input=input("You: ").strip()
        if user_input.lower() in ("exit", "quit", "bye"): 
            print("Bye!") 
            break
        else:
            run_agent(user_input)

