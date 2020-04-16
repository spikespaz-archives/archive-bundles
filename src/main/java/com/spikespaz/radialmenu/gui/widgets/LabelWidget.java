package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import net.minecraft.client.gui.FontRenderer;

import java.util.Arrays;
import java.util.EnumSet;

public class LabelWidget extends Widget {
    private final FontRenderer fontRenderer;
    @Getter
    @Setter
    @NonNull
    protected String text;
    @Getter
    @Setter
    protected int textColor;
    @Getter
    @Setter
    @NonNull
    protected EnumSet<Align> alignment;
    @Getter
    @Setter
    protected int vPadding, hPadding;

    public LabelWidget(FontRenderer fontRenderer) {
        this.fontRenderer = fontRenderer;
        this.text = "";
        this.textColor = 0xFFFFFFFF;
        this.alignment = EnumSet.of(Align.CH, Align.CV);
        this.hPadding = 0;
        this.vPadding = 0;
    }

    @Override
    public void draw(float partialTicks) {
        double sx, sy, sw, sh;

        sw = this.fontRenderer.getStringWidth(this.text);
        sh = this.fontRenderer.FONT_HEIGHT;

        if (this.alignment.contains(Align.L))
            sx = this.x + this.hPadding;
        else if (this.alignment.contains(Align.R))
            sx = this.x + this.width - this.hPadding;
        else
            sx = this.x + this.width / 2 - sw / 2;

        if (this.alignment.contains(Align.T))
            sy = this.y + this.vPadding;
        else if (this.alignment.contains(Align.B))
            sy = this.y + this.height - this.vPadding - sh;
        else
            sy = this.y + this.height / 2 - sh / 2;

//        sx = this.x;
//        sy = this.y;

        this.drawString(fontRenderer, this.text, (int) sx, (int) sy, this.textColor);
    }

    public static class LabelWidgetBuilder<T extends LabelWidgetBuilder, W extends LabelWidget> extends WidgetBuilder<T, W> {
        public T text(String text) {
            this.widget.setText(text);
            return (T) this;
        }

        public T color(int color) {
            this.widget.setTextColor(color);
            return (T) this;
        }

        public T vPad(int v) {
            this.widget.setVPadding(v);
            return (T) this;
        }

        public T hPad(int h) {
            this.widget.setHPadding(h);
            return (T) this;
        }

        public T pad(int v, int h) {
            this.widget.setVPadding(v);
            this.widget.setHPadding(h);
            return (T) this;
        }

        public T align(Align... alignments) {
            this.widget.setAlignment(EnumSet.of(alignments[0], Arrays.copyOfRange(alignments, 1, alignments.length)));
            return (T) this;
        }
    }
}
