package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import net.minecraft.client.gui.FontRenderer;

import java.util.Arrays;
import java.util.EnumSet;

public class LabelWidget extends Widget {
    public static final int FONT_SHADOW_HEIGHT = 1;
    protected final FontRenderer fontRenderer;
    @Getter @Setter @NonNull
    protected String text;
    @Getter @Setter
    protected int textColor;
    @Getter @Setter @NonNull
    protected EnumSet<Align> align;
    @Getter @Setter
    protected int vPadding, hPadding;

    public LabelWidget(FontRenderer fontRenderer) {
        super();
        this.fontRenderer = fontRenderer;
        this.text = "";
        this.textColor = 0xFFFFFFFF;
        this.align = EnumSet.of(Align.T, Align.B, Align.L, Align.R);
        this.hPadding = 0;
        this.vPadding = 0;
//        this.debugColor = Utilities.shiftHue(this.debugColor, 5f);
    }

    public static Builder<?, ?> build(FontRenderer fontRenderer) {
        return new Builder<>(new LabelWidget(fontRenderer));
    }

    @Override
    public void draw(double mouseX, double mouseY, float partialTicks) {
        if (!this.visible)
            return;

        super.draw(mouseX, mouseY, partialTicks);

        double sx = this.x, sy = this.y, tw, th;

        tw = this.fontRenderer.getStringWidth(this.text);
        th = this.fontRenderer.FONT_HEIGHT;

        boolean stackLeft = this.align.contains(Align.L);
        boolean stackRight = this.align.contains(Align.R);
        boolean stackTop = this.align.contains(Align.T);
        boolean stackBottom = this.align.contains(Align.B);

        if (stackLeft && stackRight)
            sx = this.x + (this.width - tw) / 2;
        else if (stackLeft)
            sx = this.x + this.hPadding;
        else if (this.align.contains(Align.R))
            sx = this.x + this.width - tw - this.hPadding;

        if (stackTop && stackBottom)
            sy = this.y + (this.height - th) / 2 + FONT_SHADOW_HEIGHT;
        else if (stackLeft)
            sy = this.y + this.vPadding;
        else if (stackRight)
            sy = this.y + this.height - th - this.vPadding;

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

        public B align(Align... aligns) {
            this.widget.setAlign(EnumSet.of(aligns[0], Arrays.copyOfRange(aligns, 1, aligns.length)));
            return this.self();
        }
    }
}
