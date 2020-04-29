package com.spikespaz.radialmenu.gui.widgets;

import com.google.common.collect.Lists;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.util.EnumSet;
import java.util.List;

public class MultiWidget extends Widget {
    @Getter
    @Setter
    protected double childWidth, childHeight;
    @Getter
    @Setter
    protected int vPadding, hPadding;
    @Getter
    @Setter
    @NonNull
    protected EnumSet<Align> align;
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
        boolean stackLeft = this.align.contains(Align.L);
        boolean stackRight = this.align.contains(Align.R);
        boolean stackTop = this.align.contains(Align.T);
        boolean stackBottom = this.align.contains(Align.B);
        boolean stackCH = this.align.contains(Align.CH);
        boolean stackCV = this.align.contains(Align.CV);

        this.update();

        for (Widget child : children)
            child.draw(mouseX, mouseY, partialTicks);
    }

    @Override
    public void drawDebug() {
        super.drawDebug();

        for (Widget child : this.children)
            child.drawDebug();
    }

    protected Widget addChild(Widget widget) {
        this.children.add(widget);
        this.update();
        return widget;
    }

    public void update() {
        boolean stackLeft = this.align.contains(Align.L);
        boolean stackRight = this.align.contains(Align.R);
        boolean stackTop = this.align.contains(Align.T);
        boolean stackBottom = this.align.contains(Align.B);
        boolean stackCH = this.align.contains(Align.CH);
        boolean stackCV = this.align.contains(Align.CV);

        if (stackLeft || stackRight || stackCH)
            this.childHeight = this.height;

        if (stackTop || stackBottom || stackCV)
            this.childWidth = this.width;

        double offsetX = 0, offsetY = 0;

        double itw = this.childWidth * this.children.size() + this.hPadding * (this.children.size() - 1);
        double ith = this.childHeight * this.children.size() + this.vPadding * (this.children.size() - 1);
        double dcw = (this.width - this.childWidth) / (this.children.size() - 1);
        double dch = (this.height - this.childHeight) / (this.children.size() - 1);

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
            else if (stackCV)
                offsetY += this.childHeight + this.vPadding;
            else if (stackTop || stackBottom)
                offsetY += this.childHeight + this.vPadding;

            if (stackLeft && stackRight)
                offsetX += dcw;
            if (stackLeft || stackRight || stackCH)
                offsetX += this.childWidth + this.hPadding;
        }
    }
}
