package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.MathHelper;
import lombok.Getter;
import lombok.Setter;
import net.minecraft.client.Minecraft;
import net.minecraft.client.audio.PositionedSoundRecord;
import net.minecraft.client.audio.SoundHandler;
import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.ScaledResolution;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.client.renderer.RenderItem;
import net.minecraft.client.resources.I18n;
import net.minecraft.client.settings.KeyBinding;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.SoundEvent;

import javax.annotation.ParametersAreNonnullByDefault;

public class GuiRadialButton extends GuiButton {
    private static final Minecraft mc = Minecraft.getMinecraft();
    protected final RenderItem itemRender;
    public int radius;
    public int deadRadius;
    public int thickness;
    public int sliceCount;
    public int sliceNum;
    public int normalColor;
    public int hoverColor;
    public double[] centroid;
    protected ItemStack itemIcon;
    protected ResourceLocation imageIcon;
    public KeyBinding keyBinding;
    private SoundEvent pressSound;
    private float pressSoundPitch;
    private float iconOpacity;
    private float hoverIconOpacity;
    public double cx;
    public double cy;
    private int normalAlpha;
    @Setter
    @Getter
    private boolean selected;
    private int currentColor;
    public boolean mouseBoundary;

    public GuiRadialButton(int buttonId, int radius, int deadRadius, int thickness, int normalColor, int hoverColor, float iconOpacity, float hoverIconOpacity) {
        super(buttonId, 0, 0, "");
        this.itemRender = mc.getRenderItem();
        this.id = buttonId;
        this.radius = radius;
        this.deadRadius = deadRadius;
        this.thickness = thickness;
        this.normalColor = normalColor;
        this.hoverColor = hoverColor;
        this.iconOpacity = iconOpacity;
        this.hoverIconOpacity = hoverIconOpacity;

        final ScaledResolution scaledRes = new ScaledResolution(mc);

        this.cx = scaledRes.getScaledWidth_double() / 2;
        this.cy = scaledRes.getScaledHeight_double() / 2;
    }

    @Override
    @ParametersAreNonnullByDefault
    public void drawButton(Minecraft mc, int mouseX, int mouseY, float partialTicks) {
        if (!this.visible) return;

        this.hovered = this.isMouseOver(mouseX, mouseY);

        final double sa = Math.PI * 2 / this.sliceCount; // Slice angle
        final double ssa = (this.sliceCount - this.sliceNum) * sa - sa / 2 + Math.PI; // Start slice angle
        final double esa = ssa + sa; // End slice angle
        final double ipr = this.radius / Math.cos(sa / 2); // Inner point radius
        final double opr = ipr + this.thickness; // Outer point radius

        final double x0 = this.cx + Math.sin(ssa) * ipr;
        final double y0 = this.cy + Math.cos(ssa) * ipr;
        final double x1 = this.cx + Math.sin(ssa) * opr;
        final double y1 = this.cy + Math.cos(ssa) * opr;
        final double x2 = this.cx + Math.sin(esa) * opr;
        final double y2 = this.cy + Math.cos(esa) * opr;
        final double x3 = this.cx + Math.sin(esa) * ipr;
        final double y3 = this.cy + Math.cos(esa) * ipr;

        double[][] vertices = new double[][]{{x0, y0}, {x1, y1}, {x2, y2}, {x3, y3}};

        this.centroid = MathHelper.centroid(vertices);

        final int normalColor = this.normalColor & 0xFFFFFF;
        final int normalAlpha = this.normalColor >> 24 & 0xFF;
        final int hoverColor = this.hoverColor & 0xFFFFFF;
        final int hoverAlpha = this.hoverColor >> 24 & 0xFF;
        final int currentColor = this.currentColor & 0xFFFFFF;
        final int currentAlpha = this.currentColor >> 24 & 0xFF;

        int alpha, color;

        if (this.hovered) {
            alpha = hoverAlpha;
            color = hoverColor;
        } else if (this.selected) {
            alpha = normalAlpha;
            color = hoverColor;
        } else {
            alpha = normalAlpha;
            color = normalColor;
        }

        this.currentColor = (alpha << 24) + color;

        RenderHelper.drawPoly(vertices, this.currentColor);

        // Uncomment to draw points in red
//        RenderHelper.drawCircle(x0, y0, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x1, y1, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x2, y2, 2D, 10, 0xFFFF0000);
//        RenderHelper.drawCircle(x3, y3, 2D, 10, 0xFFFF0000);

        // Uncomment to draw the a dot in the center of each button
//        RenderHelper.drawCircle(this.centroid[0], this.centroid[1], 5, 10, 0xFF00FFFF);

        if (this.imageIcon != null && this.imageIcon.getPath().endsWith(".png") && !this.imageIcon.getNamespace().isEmpty()) {
            mc.getTextureManager().bindTexture(this.imageIcon);
            GlStateManager.color(1, 1, 1);
            Gui.drawModalRectWithCustomSizedTexture((int) this.centroid[0] - 8, (int) this.centroid[1] - 8, 0, 0, 16, 16, 16, 16);
        } else if (this.itemIcon != null) {
            net.minecraft.client.renderer.RenderHelper.enableGUIStandardItemLighting();
            this.itemRender.renderItemIntoGUI(itemIcon, (int) this.centroid[0] - 8, (int) this.centroid[1] - 8);
            net.minecraft.client.renderer.RenderHelper.disableStandardItemLighting();
        }

        this.mouseDragged(mc, mouseX, mouseY);
    }

    @Override
    public boolean mousePressed(Minecraft mc, int mouseX, int mouseY) {
        return this.enabled && this.visible && this.isMouseOver(mouseX, mouseY);
    }

    private boolean isMouseOver(int mouseX, int mouseY) {
        final double sa = Math.PI * 2 / this.sliceCount; // Slice angle
        final double ssa = (this.sliceCount - this.sliceNum) * sa - sa / 2 + Math.PI; // Start slice angle
        final double esa = ssa + sa; // End slice angle

        final double mr = Math.hypot(mouseX - this.cx, mouseY - this.cy); // Mouse radius
        final double ma = Math.atan2(mouseX - this.cx, mouseY - this.cy); // Mouse angle

        if (this.mouseBoundary && mr > this.thickness + this.radius)
            return false;

        return MathHelper.isAngleBetween(ssa, esa, ma) && mr > this.deadRadius;
    }

    @Override
    public boolean isMouseOver() {
        return this.hovered;
    }

    public void setPressSound(SoundEvent sound, float pitch) {
        this.pressSound = sound;
        this.pressSoundPitch = pitch;
    }

    @Override
    public void playPressSound(SoundHandler soundHandlerIn) {
        soundHandlerIn.playSound(PositionedSoundRecord.getMasterRecord(this.pressSound, this.pressSoundPitch));
    }

    public void setKeyBinding(KeyBinding binding) {
        if (binding == null) {
            this.displayString = "";
            this.keyBinding = null;
        } else {
            this.displayString = I18n.format(binding.getKeyDescription());
            this.keyBinding = binding;
        }
    }

    public void setIcon(Item item) {
        this.itemIcon = new ItemStack(item);
        this.imageIcon = null;
    }

    public void setIcon(ResourceLocation resource) {
        this.imageIcon = resource;
        this.itemIcon = null;
    }
}
