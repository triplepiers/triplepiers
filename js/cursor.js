const cursors = [
    document.getElementById("cursor-inner"),
    // document.getElementById("cursor-outter")
];


function moveCursors(e) {
    let { clientX, clientY } = e;
    cursors.forEach((cursor) => {
        cursor.style.left = `${clientX}px`;
        cursor.style.top = `${clientY}px`;
    })
}

export {
    moveCursors
}