package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import net.minecraft.client.gui.FontRenderer;

import java.util.Arrays;
import java.util.EnumSet;

public class LabelWidget extends Widget {
    public static final int FONT_SHADOW_HEIGHT = 1;
    private final FontRenderer fontRenderer;
    @Getter @Setter @NonNull
    protected String text;
    @Getter @Setter
    protected int textColor;
    @Getter @Setter @NonNull
    protected EnumSet<Align> alignment;
    @Getter @Setter
    protected int vPadding, hPadding;

    public LabelWidget(FontRenderer fontRenderer) {
        this.fontRenderer = fontRenderer;
        this.text = "";
        this.textColor = 0xFFFFFFFF;
        this.alignment = EnumSet.of(Align.CH, Align.CV);
        this.hPadding = 0;
        this.vPadding = 0;
    }

    public static Builder<?, ?> build(FontRenderer fontRenderer) {
        return new Builder<>(new LabelWidget(fontRenderer));
    }

    @Override
    public void draw(double mouseX, double mouseY, float partialTicks) {
        if (!this.visible)
            return;

        double sx, sy, tw, th;

        tw = this.fontRenderer.getStringWidth(this.text);
        th = this.fontRenderer.FONT_HEIGHT;

        if (this.alignment.contains(Align.L))
            sx = this.x + this.hPadding;
        else if (this.alignment.contains(Align.R))
            sx = this.x + this.width - tw - this.hPadding;
        else
            sx = this.x + (this.width - tw) / 2;

        if (this.alignment.contains(Align.T))
            sy = this.y + this.vPadding;
        else if (this.alignment.contains(Align.B))
            sy = this.y + this.height - th - this.vPadding;
        else
            sy = this.y + (this.height - th) / 2 + FONT_SHADOW_HEIGHT;

        fontRenderer.drawStringWithShadow(this.text, (int) sx, (int) sy, this.textColor);
    }

    public static class Builder<W extends LabelWidget, B extends Builder<W, B>> extends Widget.Builder<W, B> {
        public Builder(W widget) {
            super(widget);
        }

        public B text(String text) {
            this.widget.setText(text);
            return this.self();
        }

        public B color(int color) {
            this.widget.setTextColor(color);
            return this.self();
        }

        public B vPad(int v) {
            this.widget.setVPadding(v);
            return this.self();
        }

        public B hPad(int h) {
            this.widget.setHPadding(h);
            return this.self();
        }

        public B pad(int v, int h) {
            this.widget.setVPadding(v);
            this.widget.setHPadding(h);
            return this.self();
        }

        public B align(Align... alignments) {
            this.widget.setAlignment(EnumSet.of(alignments[0], Arrays.copyOfRange(alignments, 1, alignments.length)));
            return this.self();
        }
    }
}
