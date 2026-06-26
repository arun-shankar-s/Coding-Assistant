async function sendMessage(){

    let input =
        document.getElementById("user-input");

    let message = input.value;

    let response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });

    let data = await response.json();

    let chat =
        document.getElementById("chat-box");

    chat.innerHTML += `
        <div>
            <b>You:</b> ${message}
        </div>

        <div>
            <b>Agent:</b> ${data.response}
        </div>
    `;

    input.value = "";

    loadMemory();
}

async function loadMemory(){

    let response =
        await fetch("/memory");

    let data =
        await response.json();

    let view =
        document.getElementById("memory-view");

    view.innerHTML =
        JSON.stringify(
            data.memory,
            null,
            2
        );
}
