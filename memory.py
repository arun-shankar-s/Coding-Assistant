class Memory:
    def __init__(self):
        self.notes=[]
    
    def get_recent(self,limit=10):
        recent=self.notes[-limit:]
        return "\n".join(
            f"[{n['category']}] {n['content']} {n['result']}"
            for n in recent
        )    
    def get_all(self)->str:
        return "\n".join(self.notes)
    
    def clear(self):
        self.notes.clear()
    
    def add(self, category, content,result):

        self.notes.append({
            "category": category,
            "content": content,
            "result":result
        })

        if len(self.notes) > 100:
            self.notes.pop(0)

    def search(self,query):
        matches=[]
        for note in self.notes:
            text=(
                str(note["category"])
                + " "
                + str(note["content"])
                + " "
                + str(note["result"])
            )
            if query.lower() in text.lower():
                matches.append(str(note))

        if not matches:
            return "No memory found"
    
        return "\n".join(matches)
    
    def has_file_summary(self,path):
        for note in self.notes:
            if (
                note["category"]=="file_summary"
                and note["content"]==path
            ):
                return True
        return False
    
    def get_file_summary(self,path):
        for note in self.notes:
            if (
                note["category"]=="file_summary"
                and note["content"]==path
            ):
                return note["result"]
        return None
    
    def upsert_file_summary(self,path,summary):
        for note in self.notes:
            if(
                note["category"]=="file_summary"
                and note["content"]==path
            ):
                note["result"]=summary
                return "updated"
        self.add(
            "file_summary",
            path,
            summary
        )
        return "created"