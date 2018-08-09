module widgets.widgets;

import arsd.nanovega;
import arsd.color;
public import widgets.themes;
public import widgets.utilities;

/// Draw a simple rectangle the color of `BACKGROUND_COLOR` on the NanoVega context.
public void drawBackground(NVGContext nvgc, Color backgroundColor, const PointF pos, const SizeF size) {
    nvgc.beginPath();
    nvgc.fillColor = backgroundColor.getNVGColor();
    nvgc.rect(pos.x, pos.y, size.width, size.height);
    nvgc.fill();
}

/// Draw a check box to a NanoVega context.
public void drawCheckBox(NVGContext nvgc, CheckBoxTheme theme, const PointF pos, const float size = 15, ushort state = UNCHECKED) {
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
    } else {
        nvgc.fillColor = theme.uncheckedFillColor;
        nvgc.strokeColor = theme.uncheckedBorderColor;
    }

    nvgc.strokeWidth = theme.borderWidth;

    if (!theme.borderRadius)
        nvgc.rect(pos.x, pos.y, size, size);
    else
        nvgc.roundedRect(pos.x, pos.y, size, size, theme.borderRadius);

    nvgc.fill();

    if (theme.borderWidth)
        nvgc.stroke();

    if (checkFlag(state, CHECKED)) {
        nvgc.beginPath();
        nvgc.rect(pos.x, pos.y, size, size);
        nvgc.fillPaint(nvgc.imagePattern(pos.x, pos.y, size, size, 0, theme.checkImage));
        nvgc.fill();
    }
}

/// Draw a radio button to a NanoVega context.
public void drawRadioButton(NVGContext nvgc, CheckBoxTheme theme, const PointF pos, const float size = 15, ushort state = UNCHECKED) {
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
    } else {
        nvgc.fillColor = theme.uncheckedFillColor;
        nvgc.strokeColor = theme.uncheckedBorderColor;
    }

    nvgc.strokeWidth = theme.borderWidth;

    const float radius = size / 2;

    nvgc.circle(pos.x + radius, pos.y + radius, radius);

    nvgc.fill();

    if (theme.borderWidth)
        nvgc.stroke();

    if (checkFlag(state, CHECKED)) {
        nvgc.beginPath();
        nvgc.rect(pos.x, pos.y, size, size);
        nvgc.fillPaint(nvgc.imagePattern(pos.x, pos.y, size, size, 0, theme.checkImage));
        nvgc.fill();
    }
}

/// Draw a text button to the NanoVega context.
public void drawButton(NVGContext nvgc, ButtonTheme theme, const string text, const PointF pos,
        const SizeF size = SizeF(70, 26), ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
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
    } else {
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

    const PointF textPos = PointF(pos.x + theme.textPadding, pos.y + theme.textPadding);
    const SizeF textSize = SizeF(size.width - theme.textPadding * 2, size.height - theme.textPadding * 2);

    nvgc.drawTextLabel(textTheme, text, textPos, textSize, state);
}

/// Draw a text label to the NanoVega context.
public void drawTextLabel(NVGContext nvgc, TextLabelTheme theme, const string text, const PointF pos,
        const SizeF size = SizeF(70, 26), ushort state = CENTER_VERTICAL | CENTER_HORIZONTAL) {
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

public void drawScrollBar(NVGContext nvgc, ScrollBarTheme theme, const PointF pos, const float height,
        float viewHeight, float viewPos, float contentHeight, ushort state = ZEROFLAG) {
    float handleHeight = (height / contentHeight) * viewHeight;
    float handlePos = ((height - handleHeight) / contentHeight) * viewPos;

    NVGColor trackColor;
    NVGColor handleColor;
    NVGColor borderColor;

    if (checkFlag(state, ACTIVE)) {
        trackColor = theme.activeTrackColor;
        handleColor = theme.activeHandleColor;
        borderColor = theme.activeBorderColor;
    } else if (checkFlag(state, HOVERED)) {
        trackColor = theme.hoveredTrackColor;
        handleColor = theme.hoveredHandleColor;
        borderColor = theme.hoveredBorderColor;
    } else {
        trackColor = theme.defaultTrackColor;
        handleColor = theme.defaultHandleColor;
        borderColor = theme.defaultBorderColor;
    }

    nvgc.beginPath();
    nvgc.fillColor = trackColor;
    nvgc.strokeColor = borderColor;
    nvgc.strokeWidth = theme.borderWidth;
    nvgc.rect(pos.x, pos.y, theme.width, height);
    nvgc.fill();
    nvgc.stroke();
    nvgc.closePath();

    nvgc.beginPath();
    nvgc.fillColor = handleColor;

    const PointF trackPos = PointF(pos.x + theme.borderPadding, pos.y + theme.borderPadding + handlePos);
    const SizeF trackSize = SizeF(theme.width - theme.borderPadding * 2, handleHeight - theme.borderPadding * 2);

    if (theme.radius)
        nvgc.roundedRect(trackPos.x, trackPos.y, trackSize.width, trackSize.height, theme.radius);
    else
        nvgc.rect(trackPos.x, trackPos.y, trackSize.width, trackSize.height);

    nvgc.fill();
}

/// Draw a text input to the NanoVega context.
public void drawTextInput(NVGContext nvgc, TextInputTheme theme, const string text, const PointF pos,
        const SizeF size = SizeF(100, 26), ushort state = CENTER_VERTICAL | ALIGN_LEFT) {
    nvgc.beginPath();
    nvgc.strokeWidth = theme.borderWidth;

    TextLabelTheme textTheme;

    if (checkFlag(state, ACTIVE)) {
        nvgc.strokeColor = theme.activeBorderColor;
        nvgc.fillColor = theme.activeBackgroundColor;
        textTheme = theme.activeTextTheme;
    } else if (checkFlag(state, HOVERED)) {
        nvgc.strokeColor = theme.hoveredBorderColor;
        nvgc.fillColor = theme.hoveredBackgroundColor;
        textTheme = theme.hoveredTextTheme;
    } else {
        nvgc.strokeColor = theme.defaultBorderColor;
        nvgc.fillColor = theme.defaultBackgroundColor;
        textTheme = theme.defaultTextTheme;
    }

    if (theme.borderRadius)
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, theme.borderRadius);
    else
        nvgc.rect(pos.x, pos.y, size.width, size.height);

    nvgc.fill();
    nvgc.stroke();

    const PointF textPos = PointF(pos.x + theme.borderPadding, pos.y + theme.borderPadding);
    const SizeF textSize = SizeF(size.width - theme.borderPadding * 2, size.height - theme.borderPadding * 2);

    nvgc.drawTextLabel(textTheme, text, textPos, textSize, state);
}
