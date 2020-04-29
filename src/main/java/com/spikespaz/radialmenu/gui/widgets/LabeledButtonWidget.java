package com.spikespaz.radialmenu.gui.widgets;

import net.minecraft.client.gui.FontRenderer;

public class LabeledButtonWidget extends MultiWidget {
    protected final FontRenderer fontRenderer;
    protected LabelWidget labelWidget0, labelWidget1;

    public LabeledButtonWidget(FontRenderer fontRenderer) {
        super();
        this.fontRenderer = fontRenderer;
        this.labelWidget0 = (LabelWidget) this.addChild(new LabelWidget(fontRenderer));
        this.labelWidget1 = (LabelWidget) this.addChild(new LabelWidget(fontRenderer));
        this.labelWidget0.setText("First Text Widget");
        this.labelWidget1.setText("Second Text Widget");
    }
}
