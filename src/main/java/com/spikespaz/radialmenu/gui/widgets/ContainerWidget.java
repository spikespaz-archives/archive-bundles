package com.spikespaz.radialmenu.gui.widgets;

import com.google.common.collect.Lists;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.util.EnumSet;
import java.util.List;

public class MultiWidget extends Widget {
    @Getter @Setter
    protected double childWidth, childHeight;
    @Getter @Setter
    protected int vPadding, hPadding;
    @Getter @Setter @NonNull
    protected EnumSet<Align> align;
    @Getter @NonNull
    protected List<Widget> children;

    public MultiWidget() {
        this.childWidth = 200;
        this.childHeight = 20;
        this.hPadding = 0;
        this.vPadding = 0;
        this.align = EnumSet.of(Align.CV);
        this.children = Lists.newArrayList();
    }

    @Override
    public void draw(double mouseX, double mouseY, float partialTicks) {
        if (!this.visible)
            return;

        super.draw(mouseX, mouseY, partialTicks);

        for (Widget child : children)
            child.draw(mouseX, mouseY, partialTicks);
    }

    @Override
    public void update() {
        boolean stackCV = false, stackCH = false, stackLeft = false, stackRight = false, stackTop = false, stackBottom = false;

        stackCV = this.align.contains(Align.CV);

        if (!stackCV)
            stackCH = this.align.contains(Align.CH);

        if (!stackCV && !stackCH) {
            stackTop = this.align.contains(Align.T);
            stackBottom = this.align.contains(Align.B);
        }

        if (!stackCV && !stackCH && !stackTop && !stackBottom) {
            stackLeft = this.align.contains(Align.L);
            stackRight = this.align.contains(Align.R);
        }

        if (stackLeft || stackRight || stackCH)
            this.childHeight = this.height;

        if (stackTop || stackBottom || stackCV)
            this.childWidth = this.width;

        double offsetX = 0, offsetY = 0;

        final double itw = this.childWidth * this.children.size() + this.hPadding * (this.children.size() - 1);
        final double ith = this.childHeight * this.children.size() + this.vPadding * (this.children.size() - 1);
        final double dcw = (this.width - this.childWidth) / (this.children.size() - 1);
        final double dch = (this.height - this.childHeight) / (this.children.size() - 1);

        if (stackCV)
            offsetY = (this.height - ith) / 2;
        else if (stackBottom && !stackTop)
            offsetY = this.height - ith - this.childHeight;

        if (stackCH)
            offsetX = (this.width - itw) / 2;
        else if (stackRight && !stackLeft)
            offsetX = this.width - itw - this.childWidth;

        for (Widget child : this.children) {
            child.setBox(this.childWidth, this.childHeight, this.x + offsetX, this.y + offsetY);

            if (stackTop && stackBottom)
                offsetY += dch;
            else if (stackCV || stackTop || stackBottom)
                offsetY += this.childHeight + this.vPadding;

            if (stackLeft && stackRight)
                offsetX += dcw;
            else if (stackCH || stackLeft || stackRight)
                offsetX += this.childWidth + this.hPadding;
        }
    }

    @Override
    public void drawDebug() {
        if (!this.visible)
            return;

        super.drawDebug();

        for (Widget child : this.children)
            child.drawDebug();
    }

    protected Widget addChild(Widget widget) {
        this.children.add(widget);
        this.update();
        return widget;
    }
}
