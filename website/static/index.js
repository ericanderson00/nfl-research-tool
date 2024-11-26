function deleteNote(noteId){
    fetch("/delete-note", {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) =>{
        window.location.href = "/notes"; //how to reload window with get request (refresh the page)
    });
}