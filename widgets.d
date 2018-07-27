import arsd.nanovega;
import arsd.color;
public import themes;
public import utilities;

/// Draw a simple rectangle the color of `BACKGROUND_COLOR` on the NanoVega context.
public void drawBackground(NVGContext nvgc, const PointF pos, const SizeF size) {
    nvgc.beginPath();
    nvgc.fillColor = BACKGROUND_COLOR.getNVGColor();
    nvgc.rect(pos.x, pos.y, size.width, size.height);
    nvgc.fill();
}

/// Draw a check box to a NanoVega context.
public void drawCheckBox(NVGContext nvgc, CheckBoxTheme theme, const PointF pos, const SizeF size = const SizeF(14f,
        14f), const ushort state = UNCHECKED) {
    nvgc.beginPath();

    if (checkFlag(state, ACTIVE)) {
        nvgc.fillColor = theme.activeFillColor;
        nvgc.strokeColor = theme.activeBorderColor;
    } else if (checkFlag(state, HOVERED)) {
        nvgc.fillColor = theme.hoveredFillColor;
        nvgc.strokeColor = theme.hoveredBorderColor;

    } else if (checkFlag(state, CHECKED)) {
        nvgc.fillColor = theme.checkedFillColor;
        nvgc.strokeColor = theme.checkedBorderColor;
    } else if (checkFlag(state, UNCHECKED) || checkFlag(state, ZEROFLAG)) {
        nvgc.fillColor = theme.uncheckedFillColor;
        nvgc.strokeColor = theme.uncheckedBorderColor;
    }

    nvgc.strokeWidth = theme.borderWidth;

    if (!theme.borderRadius)
        nvgc.rect(pos.x, pos.y, size.width, size.height);
    else
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, theme.borderRadius);

    nvgc.fill();

    if (theme.borderWidth)
        nvgc.stroke();
}

/// Draw a text button to the NanoVega context.
public void drawButton(NVGContext nvgc, ButtonTheme theme, const string text, const PointF pos,
        const SizeF size = SizeF(70f, 26f), const ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
    nvgc.beginPath();

    TextLabelTheme textTheme;

    if (checkFlag(state, ACTIVE)) {
        nvgc.fillColor = theme.activeFillColor;
        nvgc.strokeColor = theme.activeBorderColor;
        textTheme = theme.activeTextTheme;
    } else if (checkFlag(state, HOVERED)) {
        nvgc.fillColor = theme.hoveredFillColor;
        nvgc.strokeColor = theme.hoveredBorderColor;
        textTheme = theme.hoveredTextTheme;
    } else if (checkFlag(state, ZEROFLAG)) {
        nvgc.fillColor = theme.defaultFillColor;
        nvgc.strokeColor = theme.defaultBorderColor;
        textTheme = theme.defaultTextTheme;
    }

    nvgc.strokeWidth = theme.borderWidth;

    if (!theme.borderRadius)
        nvgc.rect(pos.x, pos.y, size.width, size.height);
    else
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, theme.borderRadius);

    nvgc.fill();

    if (theme.borderWidth)
        nvgc.stroke();

    PointF textPos = PointF(pos.x + theme.textPadding, pos.y + theme.textPadding);
    SizeF textSize = SizeF(size.width - theme.textPadding * 2, size.height - theme.textPadding * 2);

    nvgc.drawTextLabel(textTheme, text, textPos, textSize, state);
}

/// Draw a text label to the NanoVega context.
public void drawTextLabel(NVGContext nvgc, TextLabelTheme theme, const string text, const PointF pos,
        const SizeF size = SizeF(70f, 26f), const ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
    if (nvgc.findFont(theme.textFont) == -1)
        nvgc.createFont(theme.textFont, "fonts/" ~ theme.textFont ~ ".ttf");

    nvgc.fontSize = theme.textSize;
    nvgc.fontBlur = theme.textBlur;
    nvgc.textLetterSpacing = theme.textSpacing;
    nvgc.fontFace(theme.textFont);
    nvgc.fillColor = theme.textColor;

    float posY = pos.y;

    NVGTextAlign.H horizontalAlign = NVGTextAlign.H.Left;
    NVGTextAlign.V verticalAlign = NVGTextAlign.V.Top;

    if (checkFlag(state, CENTER_VERTICAL)) {
        posY += (size.height / 2);
        verticalAlign = NVGTextAlign.V.Middle;
    } else if (checkFlag(state, ALIGN_TOP)) {
        verticalAlign = NVGTextAlign.V.Top;
    } else if (checkFlag(state, ALIGN_BOTTOM)) {
        posY += size.height;
        verticalAlign = NVGTextAlign.V.Bottom;
    }

    if (checkFlag(state, CENTER_HORIZONTAL)) {
        horizontalAlign = NVGTextAlign.H.Center;
    } else if (checkFlag(state, ALIGN_LEFT)) {
        horizontalAlign = NVGTextAlign.H.Left;
    } else if (checkFlag(state, ALIGN_RIGHT)) {
        horizontalAlign = NVGTextAlign.H.Right;
    }

    nvgc.textAlign(verticalAlign, horizontalAlign);
    nvgc.textBox(pos.x, posY, size.width, text);
}

/// Draw a check box to a NanoVega context, according to the active theme global `theme`.
public void drawCheckBox(NVGContext nvgc, const PointF pos, const SizeF size = const SizeF(14f, 14f), const ushort state = UNCHECKED) {
    nvgc.drawCheckBox(CHECK_BOX_THEME, pos, size, state);
}

/// Draw a text button to the NanoVega context, according to the theme global `TEXT_BUTTON_THEME`.
public void drawButton(NVGContext nvgc, const string text, const PointF pos, const SizeF size = SizeF(70f, 26f),
        const ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
    nvgc.drawButton(TEXT_BUTTON_THEME, text, pos, size, state);
}

/// Draw a text label to the NanoVega context, according to the theme global `TEXT_LABEL_THEME`.
public void drawTextLabel(NVGContext nvgc, const string text, const PointF pos, const SizeF size = SizeF(70f, 26f),
        const ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
    nvgc.drawTextLabel(TEXT_LABEL_THEME, text, pos, size, state);

    // // Debug
    // float[4] textBounds;
    // nvgc.textBoxBounds(pos.x, pos.y, size.width, text, textBounds);

    // float textHeight = textBounds[3] - textBounds[1];
    // float textWidth = textBounds[2] - textBounds[0];

    // // Debug text bounds
    // nvgc.beginPath();
    // nvgc.strokeWidth = 1;
    // nvgc.strokeColor = NVGColor.red;
    // nvgc.rect(pos.x, posY - textHeight, textWidth, textHeight);
    // nvgc.stroke();

    // // Debug bounding box
    // nvgc.beginPath();
    // nvgc.strokeWidth = 1;
    // nvgc.strokeColor = NVGColor.blue;
    // nvgc.rect(pos.x, pos.y, size.width, size.height);
    // nvgc.stroke();
}
