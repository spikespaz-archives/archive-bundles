package com.spikespaz.radialmenu.gui;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.renderer.BufferBuilder;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.client.renderer.vertex.DefaultVertexFormats;

public class GuiEditRadialMenu extends GuiRadialMenu {
    private static final int ADD_BUTTON = 101;
    private static final int DELETE_BUTTON = 102;
    private static final int btnW = 150;
    private static final int btnH = 20;
    protected int editsX;
    private boolean reInitGui;
    private int lastSelectedButtonId;

    public GuiEditRadialMenu(Minecraft mc) {
        super(mc);
    }

    @Override
    protected GuiRadialButton addButton(int id, int circleRadius, int deadZoneRadius, int buttonThickness, int buttonBgColor, int buttonBgHoverColor, float iconOpacity, float hoverIconOpacity) {
        if (circleRadius * 2 + buttonThickness * 2 + 10 > this.width / 2)
            circleRadius = this.width / 4 - buttonThickness - 10;

        GuiRadialButton button = super.addButton(id, circleRadius, deadZoneRadius, buttonThickness, buttonBgColor, buttonBgHoverColor, iconOpacity, hoverIconOpacity);
        button.mouseBoundary = true;
        return button;
    }

    @Override
    public void initGui() {
        super.initGui();

//        this.addButton(new GuiButton(100, this.editsX - btnW / +2, this.height / 2 - btnH / 2, btnW, btnH, "Add Button"));
        this.addButton(new GuiButton(ADD_BUTTON, this.width / 2 + 4, this.height - btnH - 4, btnH, btnH, "+"));
        this.addButton(new GuiButton(DELETE_BUTTON, this.width / 2 + 8 + btnH, this.height - btnH - 4, btnH, btnH, "-"));

        this.menuX = this.width / 4;
        this.menuY = this.height / 2;
        this.editsX = (this.width / 4) * 3;

        for (GuiButton button : this.buttonList)
            if (button instanceof GuiRadialButton) {
                if (button.id == this.lastSelectedButtonId)
                    ((GuiRadialButton) button).setSelected(true);

                ((GuiRadialButton) button).cx = this.menuX;
                ((GuiRadialButton) button).cy = this.menuY;
            } else if (button != null) {
//                button.x = this.editsX - button.width / 2;
            }
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        if (this.reInitGui) {
            this.initGui();
            this.reInitGui = false;
        }

        this.drawDefaultBackground();

        super.drawScreen(mouseX, mouseY, partialTicks);
    }

    @Override
    public boolean doesGuiPauseGame() {
        return true;
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        if (guiButton instanceof GuiRadialButton) {
            GuiRadialButton button = (GuiRadialButton) guiButton;

//        if (ConfigHandler.SOUND.isButtonSoundEnabled())
//            button.playPressSound(this.mc.getSoundHandler());

            button.setSelected(true);
            this.lastSelectedButtonId = button.id;

            for (GuiButton guiButton1 : this.buttonList)
                if ((guiButton1 instanceof GuiRadialButton) && !guiButton.equals(guiButton1))
                    ((GuiRadialButton) guiButton1).setSelected(false);
        } else {
            GuiRadialButton radialBtn = this.getSelectedButton();
            this.lastSelectedButtonId = radialBtn.id;

            switch (guiButton.id) {
                case ADD_BUTTON:
                    keyBindings.add(radialBtn.id, null);
                    buttonIcons.add(radialBtn.id, null);
                    this.reInitGui = true;
                    break;
                case DELETE_BUTTON:
                    keyBindings.remove(radialBtn.id);
                    buttonIcons.remove(radialBtn.id);
                    this.reInitGui = true;
                    break;
            }
        }
    }

    @Override
    public void drawWorldBackground(int tint) {
        if (this.mc.world != null) {
            this.drawGradientRect(0, 0, this.width, this.height, -1072689136, -804253680);
            this.drawBackground(this.width / 2, 0, this.width, this.height, tint);
        } else {
            this.drawBackground(0, 0, this.width, this.height, tint);
        }
    }

    private void drawBackground(int x0, int y0, int x1, int y1, int tint) {
        GlStateManager.disableLighting();
        GlStateManager.disableFog();
        Tessellator tessellator = Tessellator.getInstance();
        BufferBuilder bufferbuilder = tessellator.getBuffer();
        this.mc.getTextureManager().bindTexture(OPTIONS_BACKGROUND);
        GlStateManager.color(1.0F, 1.0F, 1.0F, 1.0F);
        float f = 32.0F;
        bufferbuilder.begin(7, DefaultVertexFormats.POSITION_TEX_COLOR);
        int width = x1 - x0, height = y1 - y0;
        bufferbuilder.pos(x0, y1, 0.0D).tex(0, height / 32f).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x1, y1, 0.0D).tex(width / 32f, height / 32f).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x1, y0, 0.0D).tex(width / 32f, 0).color(64, 64, 64, 255).endVertex();
        bufferbuilder.pos(x0, y0, 0.0D).tex(0, 0).color(64, 64, 64, 255).endVertex();
        tessellator.draw();
    }
}
