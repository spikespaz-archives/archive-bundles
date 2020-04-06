package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.MathHelper;
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
    public double[] centroid;

    public GuiRadialButton(int buttonId, int radius, int deadRadius, int thickness, int sliceCount, int sliceNum, int color, int hoverColor) {
        this(buttonId, radius, deadRadius, thickness, color, hoverColor);
        this.thickness = thickness;
        this.sliceCount = sliceCount;
        this.sliceNum = sliceNum;
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

        this.hovered = this.isMouseOver(mc, mouseX, mouseY);

        final ScaledResolution scaledRes = new ScaledResolution(mc);

        final double cx = scaledRes.getScaledWidth_double() / 2;
        final double cy = scaledRes.getScaledHeight_double() / 2;

        final double sa = Math.PI * 2 / this.sliceCount; // Slice angle
        final double ssa = (this.sliceCount - this.sliceNum) * sa - sa / 2 + Math.PI; // Start slice angle
        final double esa = ssa + sa; // End slice angle
        final double ipr = this.radius / Math.cos(sa / 2); // Inner point radius
        final double opr = ipr + this.thickness; // Outer point radius

        final double x0 = cx + Math.sin(ssa) * ipr;
        final double y0 = cy + Math.cos(ssa) * ipr;
        final double x1 = cx + Math.sin(ssa) * opr;
        final double y1 = cy + Math.cos(ssa) * opr;
        final double x2 = cx + Math.sin(esa) * opr;
        final double y2 = cy + Math.cos(esa) * opr;
        final double x3 = cx + Math.sin(esa) * ipr;
        final double y3 = cy + Math.cos(esa) * ipr;

        double[][] vertices = new double[][]{{x0, y0}, {x1, y1}, {x2, y2}, {x3, y3}};

        this.centroid = MathHelper.centroid(vertices);

        RenderHelper.drawPoly(vertices, this.hovered ? this.hoverColor : this.color);

        // Uncomment to draw points in red
//        RenderHelper.drawCircle(x0, y0, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x1, y1, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x2, y2, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x3, y3, 2D, 10, 0xFFFF0000);

        // Uncomment to draw the a dot in the center of each button
        RenderHelper.drawCircle(this.centroid[0], this.centroid[1], 5, 10, 0xFF00FFFF);

        this.mouseDragged(mc, mouseX, mouseY);
    }

    @Override
    public boolean mousePressed(Minecraft mc, int mouseX, int mouseY) {
        return this.enabled && this.visible && this.isMouseOver(mc, mouseX, mouseY);
    }

    private boolean isMouseOver(Minecraft mc, int mouseX, int mouseY) {
        final ScaledResolution scaledRes = new ScaledResolution(mc);

        final double cx = scaledRes.getScaledWidth_double() / 2;
        final double cy = scaledRes.getScaledHeight_double() / 2;

        final double sa = Math.PI * 2 / this.sliceCount; // Slice angle
        final double ssa = (this.sliceCount - this.sliceNum) * sa - sa / 2 + Math.PI; // Start slice angle
        final double esa = ssa + sa; // End slice angle

        final double mr = Math.hypot(mouseX - cx, mouseY - cy); // Mouse radius
        final double ma = Math.atan2(mouseX - cx, mouseY - cy); // Mouse angle

        return MathHelper.isAngleBetween(ssa, esa, ma) && mr > this.deadRadius;
    }

    @Override
    public boolean isMouseOver() {
        return this.hovered;
    }
}
