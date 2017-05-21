const canvas = document.getElementById("scaffold");
const drawing = canvas.getContext("2d");

drawing.lineWidth = 6;
drawing.lineCap = "round";

// Base
drawing.moveTo(30, 470);
drawing.lineTo(370, 470);
// Vertical Line
drawing.moveTo(120, 470);
drawing.lineTo(120, 30);
// Top Line
drawing.lineTo(250, 30);
// Hook
drawing.lineTo(250, 90);
drawing.stroke();

function drawPart(part) {
    switch (part) {
        case "head":
            drawing.moveTo(280, 120);
            drawing.arc(250, 120, 30, 0, Math.PI * 2, true);
            break;
        case "body":
            drawing.moveTo(250, 150);
            drawing.lineTo(250, 290);
            break;
        case "left_arm":
            drawing.moveTo(250, 190);
            drawing.lineTo(300, 160);
            break;
        case "right_arm":
            drawing.moveTo(250, 190);
            drawing.lineTo(200, 160);
            break;
        case "left_leg":
            drawing.moveTo(250, 290);
            drawing.lineTo(300, 320);
            break;
        case "right_leg":
            drawing.moveTo(250, 290);
            drawing.lineTo(200, 320);
            break;
    }
    drawing.stroke()
}


drawPart("head");
drawPart("body");
drawPart("left_arm");
drawPart("right_arm");
drawPart("left_leg");
drawPart("right_leg");

