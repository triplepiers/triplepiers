const cursors = [
    "#cursor-inner",
    // "#cursor-outter"
].map((tag) => { return document.querySelector(tag); });

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