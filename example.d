import arsd.simpledisplay;
import arsd.nanovega;
import arsd.color;
import widgets.widgets;
import std.stdio: writeln;
import std.conv: to;

float scrollPosition = 0;

/// Function to draw all implimented widgets to the NanoVega context.
void drawWindow(SimpleWindow swnd, NVGContext nvgc) {
    // Draw the background.
    nvgc.drawBackground(BACKGROUND_COLOR, PointF(0, 0), SizeF(swnd.width, swnd.height));

    // Draw all checkbox states.
    nvgc.drawCheckBox(CHECK_BOX_THEME, PointF(15, 15), 15, UNCHECKED);
    nvgc.drawCheckBox(CHECK_BOX_THEME, PointF(45, 15), 15, CHECKED);
    nvgc.drawCheckBox(CHECK_BOX_THEME, PointF(75, 15), 15, HOVERED);
    nvgc.drawCheckBox(CHECK_BOX_THEME, PointF(105, 15), 15, ACTIVE);

    // Draw all button states.
    nvgc.drawButton(TEXT_BUTTON_THEME, "Button", PointF(15, 45), SizeF(105, 25));
    nvgc.drawButton(TEXT_BUTTON_THEME, "HoveredButton", PointF(15, 80), SizeF(105, 25), CENTER_VERTICAL | CENTER_HORIZONTAL | HOVERED);
    nvgc.drawButton(TEXT_BUTTON_THEME, "ActiveButton", PointF(15, 115), SizeF(105, 25), CENTER_VERTICAL | CENTER_HORIZONTAL | ACTIVE);

    // Draw boxes to show the alignment of text.
    nvgc.beginPath();
    nvgc.strokeColor = NVGColor.black;
    nvgc.strokeWidth = 1;
    nvgc.rect(swnd.width - 315, 15, 150, 50);
    nvgc.rect(swnd.width - 165, 15, 150, 50);
    nvgc.rect(swnd.width - 315, 65, 150, 50);
    nvgc.rect(swnd.width - 165, 65, 150, 50);
    nvgc.rect(swnd.width - 315, 115, 150, 50);
    nvgc.rect(swnd.width - 165, 115, 150, 50);
    nvgc.rect(swnd.width - 315, 165, 150, 50);
    nvgc.rect(swnd.width - 165, 165, 150, 50);
    nvgc.rect(swnd.width - 240, 215, 150, 50);
    nvgc.stroke();
    nvgc.closePath();

    // Draw all alignments of text labels.
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Top Left", PointF(swnd.width - 315, 15), SizeF(150, 50), ALIGN_TOP | ALIGN_LEFT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Top Right", PointF(swnd.width - 165, 15), SizeF(150, 50), ALIGN_TOP | ALIGN_RIGHT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Middle Left", PointF(swnd.width - 315, 65), SizeF(150, 50), CENTER_VERTICAL | ALIGN_LEFT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Middle Right", PointF(swnd.width - 165, 65), SizeF(150, 50), CENTER_VERTICAL | ALIGN_RIGHT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Bottom Left", PointF(swnd.width - 315, 115), SizeF(150, 50), ALIGN_BOTTOM | ALIGN_LEFT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Bottom Right", PointF(swnd.width - 165, 115), SizeF(150, 50), ALIGN_BOTTOM | ALIGN_RIGHT);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Top Middle", PointF(swnd.width - 315, 165), SizeF(150, 50), ALIGN_TOP | CENTER_HORIZONTAL);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Bottom Middle", PointF(swnd.width - 165, 165), SizeF(150, 50), ALIGN_BOTTOM | CENTER_HORIZONTAL);
    nvgc.drawTextLabel(TEXT_LABEL_THEME, "Center", PointF(swnd.width - 240, 215), SizeF(150, 50), CENTER_VERTICAL | CENTER_HORIZONTAL);

    // Draw all scrollbars.
    nvgc.drawScrollBar(SCROLL_BAR_THEME, PointF(300, 0), swnd.height - 50, swnd.height, scrollPosition, 2000, ZEROFLAG);
    nvgc.drawScrollBar(SCROLL_BAR_THEME, PointF(315, 0), swnd.height - 50, swnd.height, 2000 - scrollPosition, 2000,
            HOVERED);
    nvgc.drawScrollBar(SCROLL_BAR_THEME, PointF(330, 0), swnd.height - 50, swnd.height, scrollPosition, 2000, ACTIVE);

    // Draw text inputs.
    nvgc.drawTextInput(TEXT_INPUT_THEME, "Send a message...", PointF(0, 200), SizeF(200, 60), ALIGN_LEFT | CENTER_VERTICAL);
    nvgc.drawTextInput(TEXT_INPUT_THEME, "Send a message...", PointF(0, 265), SizeF(200, 60), CENTER_HORIZONTAL | CENTER_VERTICAL | HOVERED);
    nvgc.drawTextInput(TEXT_INPUT_THEME, "Send a message...", PointF(0, 330), SizeF(200, 60), ALIGN_LEFT | CENTER_VERTICAL | ACTIVE);
}

void main() {
    NVGContext nvgc;

    setOpenGLContextVersion(3, 0);

    auto swnd = new SimpleWindow(1280, 720, "New Style Widgets", OpenGlOptions.yes, Resizability.allowResizing);

    swnd.minWidth = 768;
    swnd.minHeight = 432;

    swnd.onClosing = delegate() { nvgc.kill(); };

    swnd.visibleForTheFirstTime = delegate() {
        nvgc = nvgCreateContext();
        nvgc.initGlobalThemes();

        if (nvgc is null)
            assert(0, "Cannot initialize Nanovega context.");
    };

    swnd.redrawOpenGlScene = delegate() {
        glViewport(0, 0, swnd.width, swnd.height);
        glClearColor(0, 0, 0, 0);
        glClear(glNVGClearFlags);

        nvgc.beginFrame(swnd.width, swnd.height);
        scope (exit)
            nvgc.endFrame();

        drawWindow(swnd, nvgc);
    };

    // dfmt off
    swnd.eventLoop(60,
        delegate() {
            if (nvgc is null)
                return;

            if (scrollPosition >= 2000)
                scrollPosition = 0;
            else
                scrollPosition += 2;

            swnd.redrawOpenGlSceneNow();
            writeln(scrollPosition);
        },
        delegate(KeyEvent event) {
            writeln(to!string(event));
        },
        delegate(MouseEvent event) {
            writeln(to!string(event));
        },
        delegate(dchar ch) {
            writeln(to!string(ch));
        }
    );
    // dfmt on

    flushGui();
}
