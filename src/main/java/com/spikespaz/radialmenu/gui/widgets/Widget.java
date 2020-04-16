package com.spikespaz.radialmenu.gui.widgets;

import lombok.Getter;
import lombok.Setter;
import net.minecraft.client.gui.Gui;

public abstract class Widget extends Gui {
    @Getter
    @Setter
    protected double x, y, width, height;

    public void drawDebug() {
        this.drawGradientRect((int) this.getLeft(), (int) this.getTop(), (int) this.getRight(), (int) this.getBottom(), 0x44FF0000, 0x44FF0000);
    }

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

    public abstract void draw(float partialTicks);

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

    public static class WidgetBuilder<T extends WidgetBuilder, W extends Widget> {
        protected W widget;

        public T start(W widget) {
            this.widget = widget;
            return (T) this;
        }

        public W build() {
            return this.widget;
        }

        public T top(double y) {
            this.widget.setY(y);
            return (T) this;
        }

        public T bottom(double y) {
            this.widget.setBottom(y);
            return (T) this;
        }

        public T left(double x) {
            this.widget.setX(x);
            return (T) this;
        }

        public T right(double x) {
            this.widget.setRight(x);
            return (T) this;
        }

        public T width(double w) {
            this.widget.setWidth(w);
            return (T) this;
        }

        public T height(double h) {
            this.widget.setHeight(h);
            return (T) this;
        }

        public T pos(int x, int y) {
            this.widget.setPos(x, y);
            return (T) this;
        }

        public T size(int w, int h) {
            this.widget.setSize(w, h);
            return (T) this;
        }

        public T box(int w, int h, int x, int y) {
            this.widget.setBox(w, h, x, y);
            return (T) this;
        }
    }

    public enum Align {
        T, B, L, R, CV, CH
    }
}
