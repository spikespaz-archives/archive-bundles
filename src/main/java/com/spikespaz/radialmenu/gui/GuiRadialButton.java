package com.spikespaz.radialmenu.gui;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.ScaledResolution;

import javax.annotation.ParametersAreNonnullByDefault;

public class GuiRadialButton extends GuiButton {
    public int radius;
    public int deadRadius;
    public int thickness;
    public int sliceCount;
    public int sliceNum;
    public int color;
    public int hoverColor;

    public GuiRadialButton(int buttonId, int radius, int deadRadius, int thickness, int sliceCount, int sliceNum, int color, int hoverColor) {
        super(buttonId, 0, 0, "");
        this.id = buttonId;
        this.radius = radius;
        this.deadRadius = deadRadius;
        this.thickness = thickness;
        this.sliceCount = sliceCount;
        this.sliceNum = sliceNum;
        this.color = color;
        this.hoverColor = hoverColor;
    }

    public GuiRadialButton(int buttonId, int radius, int deadRadius, int thickness, int color, int hoverColor) {
        super(buttonId, 0, 0, "");
        this.id = buttonId;
        this.radius = radius;
        this.deadRadius = deadRadius;
        this.thickness = thickness;
        this.color = color;
        this.hoverColor = hoverColor;
    }

    @Override
    @ParametersAreNonnullByDefault
    public void drawButton(Minecraft mc, int mouseX, int mouseY, float partialTicks) {
        if (!this.visible) return;

        this.hovered = this.isMouseOver(mouseX, mouseY);

        final ScaledResolution scaledRes = new ScaledResolution(mc);

        this.sliceCount = 7;

        final double cx = scaledRes.getScaledWidth_double() / 2;
        final double cy = scaledRes.getScaledHeight_double() / 2;

        final double sa = Math.PI * 2 / this.sliceCount; // Slice angle
        final double ssa = this.sliceNum * sa - sa / 2; // Start slice angle
        final double esa = ssa + sa; // End slice angle
        final double ipr = this.radius / Math.cos(sa / 2); // Inner point radius
        final double opr = ipr + this.thickness; // Outer point radius

        final double x3 = cx + Math.sin(ssa) * ipr;
        final double y3 = cy - Math.cos(ssa) * ipr;
        final double x2 = cx + Math.sin(ssa) * opr;
        final double y2 = cy - Math.cos(ssa) * opr;
        final double x1 = cx + Math.sin(esa) * opr;
        final double y1 = cy - Math.cos(esa) * opr;
        final double x0 = cx + Math.sin(esa) * ipr;
        final double y0 = cy - Math.cos(esa) * ipr;

        final double[][] vertices = new double[][] {
                {x0, y0},
                {x1, y1},
                {x2, y2},
                {x3, y3}
        };

        RenderHelper.drawPoly(vertices, this.hovered ? this.hoverColor : this.color);

        // Uncomment to draw points in red
//        RenderHelper.drawCircle(x0, y0, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x1, y1, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x2, y2, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x3, y3, 2D, 10, 0xFFFF0000);
    }

    @Override
    public boolean mousePressed(Minecraft mc, int mouseX, int mouseY) {
        return this.enabled && this.visible && this.isMouseOver(mouseX, mouseY);
    }

    private boolean isMouseOver(int mouseX, int mouseY) {
        final double sliceAngle = Math.toRadians(360) / this.sliceCount;
        final double beginAngle = sliceAngle * this.sliceNum - sliceAngle / 2;
        final double endAngle = sliceAngle * this.sliceNum + sliceAngle / 2;

        final double polarRadius = Math.hypot(mouseX, mouseY);
        final double angle = Math.atan2(mouseY, mouseX);

        return angle >= beginAngle && angle <= endAngle && polarRadius <= this.radius + this.thickness && polarRadius >= this.deadRadius;
    }

    @Override
    public boolean isMouseOver() {
        return this.hovered;
    }
}
