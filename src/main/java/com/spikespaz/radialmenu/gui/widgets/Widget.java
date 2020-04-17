package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import lombok.Setter;
import net.minecraft.client.gui.Gui;

public abstract class Widget extends Gui {
    @Getter @Setter
    protected double x, y, width, height;
    @Getter @Setter
    protected boolean visible = true;

    public double getTop() {
        return this.y;
    }

    public double getBottom() {
        return this.y + this.height;
    }

    public double getLeft() {
        return this.x;
    }

    public double getRight() {
        return this.x + this.width;
    }

    public void setBottom(double y) {
        this.y = y - this.height;
    }

    public void setRight(double x) {
        this.x = x - this.width;
    }

    public void setPos(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void setSize(int w, int h) {
        this.width = w;
        this.height = h;
    }

    public void setBox(int w, int h, int x, int y) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
    }

    public abstract void draw(double mouseX, double mouseY, float partialTicks);

    public void drawDebug() {
        this.drawGradientRect((int) this.getLeft(), (int) this.getTop(), (int) this.getRight(), (int) this.getBottom(), 0x44FF0000, 0x44FF0000);
    }

    static abstract class Builder<W extends Widget, B extends Builder<W, B>> {
        protected W widget;

        @SuppressWarnings("unchecked")
        protected final B self() {
            return (B) this;
        }

        public Builder(W widget) {
            this.widget = widget;
        }

        public W done() {
            return this.widget;
        }

        public B visible(boolean v) {
            this.widget.setVisible(v);
            return this.self();
        }

        public B top(double y) {
            this.widget.setY(y);
            return this.self();
        }

        public B bottom(double y) {
            this.widget.setBottom(y);
            return this.self();
        }

        public B left(double x) {
            this.widget.setX(x);
            return this.self();
        }

        public B right(double x) {
            this.widget.setRight(x);
            return this.self();
        }

        public B width(double w) {
            this.widget.setWidth(w);
            return this.self();
        }

        public B height(double h) {
            this.widget.setHeight(h);
            return this.self();
        }

        public B pos(int x, int y) {
            this.widget.setPos(x, y);
            return this.self();
        }

        public B size(int w, int h) {
            this.widget.setSize(w, h);
            return this.self();
        }

        public B box(int w, int h, int x, int y) {
            this.widget.setBox(w, h, x, y);
            return this.self();
        }
    }

    public enum Align {
        T, B, L, R, CV, CH
    }
}
