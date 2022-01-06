package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.FontRenderer;

public class ButtonWidget extends Widget {
    protected final Minecraft mc;
    protected final FontRenderer fontRenderer;
    @Getter
    protected LabelWidget labelWidget;

    public ButtonWidget(Minecraft mc, FontRenderer fontRenderer) {
        super();
        this.mc = mc;
        this.fontRenderer = fontRenderer;
        this.labelWidget = LabelWidget.build(this.fontRenderer).box(this.width, this.height, this.x, this.y).done();
    }

    @Override
    public void draw(double mouseX, double mouseY, float partialTicks) {
        if (!this.visible)
            return;

        super.draw(mouseX, mouseY, partialTicks);

        this.labelWidget.draw(mouseX, mouseY, partialTicks);
    }

    @Override
    public void update() {
        this.labelWidget.setBox(this.width, this.height, this.x, y);
    }
}
