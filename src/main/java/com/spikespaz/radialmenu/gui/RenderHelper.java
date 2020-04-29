package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.Utilities;
import net.minecraft.client.renderer.BufferBuilder;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.client.renderer.vertex.DefaultVertexFormats;
import org.lwjgl.opengl.GL11;

public class RenderHelper {
    public static void drawLine(double x0, double y0, double x1, double y1, float zLevel, int color) {
        final int[] argb = Utilities.intToArgb(color);
        final float alpha = argb[0] / 255f, red = argb[1] / 255f, green = argb[2] / 255f, blue = argb[3] / 255f;

        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferBuilder = tessellator.getBuffer();

        GlStateManager.enableBlend();
        GlStateManager.disableTexture2D();
        GlStateManager.tryBlendFuncSeparate(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE_MINUS_SRC_ALPHA, GlStateManager.SourceFactor.ONE, GlStateManager.DestFactor.ZERO);
        GlStateManager.color(red, green, blue, alpha);

        bufferBuilder.begin(GL11.GL_LINES, DefaultVertexFormats.POSITION);

        bufferBuilder.pos(x0, y0, zLevel).endVertex();
        bufferBuilder.pos(x1, y1, zLevel).endVertex();

        tessellator.draw();

        GlStateManager.enableTexture2D();
        GlStateManager.disableBlend();
    }

    public static void drawHLine(double x, double y, double height, float zLevel, int color) {
        drawLine(x, y, x, y + height, zLevel, color);
    }

    public static void drawVLine(double x, double y, double width, float zLevel, int color) {
        drawLine(x, y, x + width, y, zLevel, color);
    }

    public static void drawPoly(double[][] points, float zLevel, int color) {
        final int[] argb = Utilities.intToArgb(color);
        final float alpha = argb[0] / 255f, red = argb[1] / 255f, green = argb[2] / 255f, blue = argb[3] / 255f;

        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferBuilder = tessellator.getBuffer();

        GlStateManager.enableBlend();
        GlStateManager.disableTexture2D();
        GlStateManager.tryBlendFuncSeparate(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE_MINUS_SRC_ALPHA, GlStateManager.SourceFactor.ONE, GlStateManager.DestFactor.ZERO);
        GlStateManager.color(red, green, blue, alpha);


        bufferBuilder.begin(GL11.GL_POLYGON, DefaultVertexFormats.POSITION);

        for (double[] point : points)
            bufferBuilder.pos(point[0], point[1], zLevel).endVertex();

        tessellator.draw();

        GlStateManager.enableTexture2D();
        GlStateManager.disableBlend();
    }

    public static void drawCircle(double cx, double cy, double radius, int resolution, float zLevel, int color) {
        double[][] vertices = new double[resolution][2];

        for (int i = 0; i < vertices.length; i++) {
            double a = Math.PI * 2 * i / vertices.length;

            vertices[i] = new double[]{
                    cx + Math.sin(a) * radius,
                    cy + Math.cos(a) * radius
            };
        }

        drawPoly(vertices, zLevel, color);
    }

    public static void drawRect(double x, double y, double width, double height, float zLevel, int color) {
        final int[] argb = Utilities.intToArgb(color);
        final float alpha = argb[0] / 255f, red = argb[1] / 255f, green = argb[2] / 255f, blue = argb[3] / 255f;

        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferBuilder = tessellator.getBuffer();

        GlStateManager.enableBlend();
        GlStateManager.disableTexture2D();
        GlStateManager.tryBlendFuncSeparate(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE_MINUS_SRC_ALPHA, GlStateManager.SourceFactor.ONE, GlStateManager.DestFactor.ZERO);
        GlStateManager.color(red, green, blue, alpha);

        bufferBuilder.begin(GL11.GL_QUADS, DefaultVertexFormats.POSITION);

        bufferBuilder.pos(x, y, zLevel).endVertex();
        bufferBuilder.pos(x, y + height, zLevel).endVertex();
        bufferBuilder.pos(x + width, y, zLevel + height).endVertex();
        bufferBuilder.pos(x + width, y, zLevel).endVertex();

        tessellator.draw();

        GlStateManager.enableTexture2D();
        GlStateManager.disableBlend();
    }

    public static void drawGradientRect(double x, double y, double width, double height, float zLevel, int startColor, int endColor) {
        final int[] startArgb = Utilities.intToArgb(startColor), endArgb = Utilities.intToArgb(endColor);
        final float[] startArgbF = {startArgb[0] / 255f, startArgb[1] / 255f, startArgb[2] / 255f, startArgb[3] / 255f};
        final float[] endArgbF = {endArgb[0] / 255f, endArgb[1] / 255f, endArgb[2] / 255f, endArgb[3] / 255f};

        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferBuilder = tessellator.getBuffer();

        GlStateManager.disableTexture2D();
        GlStateManager.enableBlend();
        GlStateManager.disableAlpha();
        GlStateManager.tryBlendFuncSeparate(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE_MINUS_SRC_ALPHA, GlStateManager.SourceFactor.ONE, GlStateManager.DestFactor.ZERO);
        GlStateManager.shadeModel(GL11.GL_SMOOTH);

        bufferBuilder.begin(GL11.GL_QUADS, DefaultVertexFormats.POSITION_COLOR);

        bufferBuilder.pos(x + width, y, zLevel).color(startArgbF[1], startArgbF[2], startArgbF[3], startArgbF[0]).endVertex();
        bufferBuilder.pos(x, y, zLevel).color(startArgbF[1], startArgbF[2], startArgbF[3], startArgbF[0]).endVertex();
        bufferBuilder.pos(x, y + height, zLevel).color(endArgbF[1], endArgbF[2], endArgbF[3], endArgbF[0]).endVertex();
        bufferBuilder.pos(x + width, y + height, zLevel + height).color(endArgbF[1], endArgbF[2], startArgbF[3], endArgbF[0]).endVertex();

        tessellator.draw();

        GlStateManager.shadeModel(GL11.GL_SMOOTH);
        GlStateManager.disableBlend();
        GlStateManager.enableAlpha();
        GlStateManager.enableTexture2D();
    }

    public static void drawRect(double x0, double y0, double x1, double y1, float zLevel, int color, boolean unused) {
        drawRect(Math.min(x0, x1), Math.min(y0, y1), Math.abs(x1 - x0), Math.abs(y1 - y0), zLevel, color);
    }

    public static void drawGradientRect(double x0, double y0, double x1, double y1, float zLevel, int startColor, int endColor, boolean unused) {
        drawGradientRect(Math.min(x0, x1), Math.min(y0, y1), Math.abs(x1 - x0), Math.abs(y1 - y0), zLevel, startColor, endColor);
    }

    /*    *//*
      Draws a textured rectangle at the current z-value.
     *//*
    public void drawTexturedModalRect(int x, int y, int textureX, int textureY, int width, int height)
    {
        float f = 0.00390625F;
        float f1 = 0.00390625F;
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX);
        bufferbuilder.pos((double)(x + 0), (double)(y + height), (double)this.zLevel).tex((double)((float)(textureX + 0) * 0.00390625F), (double)((float)(textureY + height) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)(y + height), (double)this.zLevel).tex((double)((float)(textureX + width) * 0.00390625F), (double)((float)(textureY + height) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)(y + 0), (double)this.zLevel).tex((double)((float)(textureX + width) * 0.00390625F), (double)((float)(textureY + 0) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(x + 0), (double)(y + 0), (double)this.zLevel).tex((double)((float)(textureX + 0) * 0.00390625F), (double)((float)(textureY + 0) * 0.00390625F)).endVertex();
        tessellator.draw();
    }

    *//*
      Draws a textured rectangle using the texture currently bound to the TextureManager
     *//*
    public void drawTexturedModalRect(float xCoord, float yCoord, int minU, int minV, int maxU, int maxV)
    {
        float f = 0.00390625F;
        float f1 = 0.00390625F;
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX);
        bufferbuilder.pos((double)(xCoord + 0.0F), (double)(yCoord + (float)maxV), (double)this.zLevel).tex((double)((float)(minU + 0) * 0.00390625F), (double)((float)(minV + maxV) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(xCoord + (float)maxU), (double)(yCoord + (float)maxV), (double)this.zLevel).tex((double)((float)(minU + maxU) * 0.00390625F), (double)((float)(minV + maxV) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(xCoord + (float)maxU), (double)(yCoord + 0.0F), (double)this.zLevel).tex((double)((float)(minU + maxU) * 0.00390625F), (double)((float)(minV + 0) * 0.00390625F)).endVertex();
        bufferbuilder.pos((double)(xCoord + 0.0F), (double)(yCoord + 0.0F), (double)this.zLevel).tex((double)((float)(minU + 0) * 0.00390625F), (double)((float)(minV + 0) * 0.00390625F)).endVertex();
        tessellator.draw();
    }

     *//*
     * Draws a texture rectangle using the texture currently bound to the TextureManager
     *//*
    public void drawTexturedModalRect(int xCoord, int yCoord, TextureAtlasSprite textureSprite, int widthIn, int heightIn)
    {
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX);
        bufferbuilder.pos((double)(xCoord + 0), (double)(yCoord + heightIn), (double)this.zLevel).tex((double)textureSprite.getMinU(), (double)textureSprite.getMaxV()).endVertex();
        bufferbuilder.pos((double)(xCoord + widthIn), (double)(yCoord + heightIn), (double)this.zLevel).tex((double)textureSprite.getMaxU(), (double)textureSprite.getMaxV()).endVertex();
        bufferbuilder.pos((double)(xCoord + widthIn), (double)(yCoord + 0), (double)this.zLevel).tex((double)textureSprite.getMaxU(), (double)textureSprite.getMinV()).endVertex();
        bufferbuilder.pos((double)(xCoord + 0), (double)(yCoord + 0), (double)this.zLevel).tex((double)textureSprite.getMinU(), (double)textureSprite.getMinV()).endVertex();
        tessellator.draw();
    }

     *//*
     * Draws a textured rectangle at z = 0. Args: x, y, u, v, width, height, textureWidth, textureHeight
     *//*
    public static void drawModalRectWithCustomSizedTexture(int x, int y, float u, float v, int width, int height, float textureWidth, float textureHeight)
    {
        float f = 1.0F / textureWidth;
        float f1 = 1.0F / textureHeight;
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX);
        bufferbuilder.pos((double)x, (double)(y + height), 0.0D).tex((double)(u * f), (double)((v + (float)height) * f1)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)(y + height), 0.0D).tex((double)((u + (float)width) * f), (double)((v + (float)height) * f1)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)y, 0.0D).tex((double)((u + (float)width) * f), (double)(v * f1)).endVertex();
        bufferbuilder.pos((double)x, (double)y, 0.0D).tex((double)(u * f), (double)(v * f1)).endVertex();
        tessellator.draw();
    }

    *//*
      Draws a scaled, textured, tiled modal rect at z = 0. This method isn't used anywhere in vanilla code.

      @param u Texture U (or x) coordinate, in pixels
     * @param v Texture V (or y) coordinate, in pixels
     * @param uWidth Width of the rendered part of the texture, in pixels. Parts of the texture outside of it will wrap
     * around
     * @param vHeight Height of the rendered part of the texture, in pixels. Parts of the texture outside of it will
     * wrap around
     * @param tileWidth total width of the texture
     * @param tileHeight total height of the texture
     *//*
    public static void drawScaledCustomSizeModalRect(int x, int y, float u, float v, int uWidth, int vHeight, int width, int height, float tileWidth, float tileHeight)
    {
        float f = 1.0F / tileWidth;
        float f1 = 1.0F / tileHeight;
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX);
        bufferbuilder.pos((double)x, (double)(y + height), 0.0D).tex((double)(u * f), (double)((v + (float)vHeight) * f1)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)(y + height), 0.0D).tex((double)((u + (float)uWidth) * f), (double)((v + (float)vHeight) * f1)).endVertex();
        bufferbuilder.pos((double)(x + width), (double)y, 0.0D).tex((double)((u + (float)uWidth) * f), (double)(v * f1)).endVertex();
        bufferbuilder.pos((double)x, (double)y, 0.0D).tex((double)(u * f), (double)(v * f1)).endVertex();
        tessellator.draw();
    }*/
}
