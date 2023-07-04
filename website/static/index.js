function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ noteId: noteId }),
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = "/";
      } else {
        console.error("Failed to delete note.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
