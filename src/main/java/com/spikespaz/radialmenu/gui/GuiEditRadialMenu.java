package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.ConfigHandler;
import com.spikespaz.radialmenu.RadialButtonData;
import com.spikespaz.radialmenu.gui.widgets.LabelWidget;
import com.spikespaz.radialmenu.gui.widgets.LabeledButtonWidget;
import com.spikespaz.radialmenu.gui.widgets.MultiWidget;
import lombok.NonNull;
import net.minecraft.client.Minecraft;
import net.minecraft.client.audio.PositionedSoundRecord;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiTextField;
import net.minecraft.client.renderer.BufferBuilder;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.client.renderer.Tessellator;
import net.minecraft.client.renderer.vertex.DefaultVertexFormats;
import net.minecraft.client.resources.I18n;
import net.minecraft.client.settings.KeyBinding;
import net.minecraft.init.SoundEvents;
import net.minecraft.util.ResourceLocation;

import java.util.Collections;

public class GuiEditRadialMenu extends GuiRadialMenu {
    private static final int ADD_BTN = 101;
    private static final int DEL_BTN = 102;
    private static final int MOVE_CCW_BTN = 103;
    private static final int MOVE_CW_BTN = 104;
    private static final int CHANGE_KEYBINDING = 110;
    private static final int CHANGE_KEYBINDING_MODE = 111;
    private static final int BTN_W = 175;
    private static final int BTN_H = 20;
    private static final int FLD_W = BTN_W - 4;
    private static final int FLD_H = BTN_H - 4;
    private static final int PAD_TOP = 8;
    private static final int PAD_LR = 8;
    private static final int PAD_OH = 4;
    private static final int OH = BTN_H * 2 + PAD_OH;
    private static final int PANEL_W = BTN_W + PAD_LR * 2;
    private static final String TOGGLE_MODE_TEXT = I18n.format("gui.radialmenu.button.togglemode");
    private static final String PRESS_MODE_TEXT = I18n.format("gui.radialmenu.button.pressmode");
    protected int editsX;
    private boolean reInitGui;
    private GuiTextField displayNameField;
    private GuiTextField iconResourceField;
    private GuiButton changeKeyBindingBtn;
    private GuiButton changeKeyModeBtn;
    private GuiCenteredTextField buttonCountField;
    private MultiWidget testWidget0;
    private MultiWidget testWidget1;
    private MultiWidget testWidget2;
    private MultiWidget testWidget3;

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

        this.menuX = (this.width - PANEL_W) / 2;
        this.menuY = this.height / 2;
        this.editsX = this.width - PANEL_W / 2;

        if (selectedButton == null)
            this.setSelectedButton(0);

        for (GuiButton guiButton : this.buttonList) {
            if (!(guiButton instanceof GuiRadialButton))
                continue;

            GuiRadialButton button = (GuiRadialButton) guiButton;

            if (button.id == this.selectedButton.id)
                button.setSelected(true);

            button.cx = this.menuX;
            button.cy = this.menuY;
        }

        this.addButton(new GuiButton(MOVE_CCW_BTN, this.editsX - BTN_H - 15 - PAD_OH - BTN_H, this.height - BTN_H - PAD_TOP, BTN_H, BTN_H, "<"));
        this.addButton(new GuiButton(ADD_BTN, this.editsX - BTN_H - 15 - PAD_OH / 2, this.height - BTN_H - PAD_TOP, BTN_H, BTN_H, "+"));
        this.buttonCountField = new GuiCenteredTextField(0, this.fontRenderer, this.editsX - 26 / 2, this.height - FLD_H - PAD_TOP - 2, 26, FLD_H);
        this.addButton(new GuiButton(DEL_BTN, this.editsX + 15 + PAD_OH / 2, this.height - BTN_H - PAD_TOP, BTN_H, BTN_H, "-"));
        this.addButton(new GuiButton(MOVE_CW_BTN, this.editsX + 15 + PAD_OH + BTN_H, this.height - BTN_H - PAD_TOP, BTN_H, BTN_H, ">"));

/*        GuiLabel label;
        int labelWidth;
        String labelString;

        labelString = I18n.format("gui.radialmenu.label.displayname");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 0, this.editsX - labelWidth / 2, PAD_TOP + OH * 0, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.displayNameField = new GuiTextField(1, this.fontRenderer, this.editsX - FLD_W / 2, PAD_TOP + OH * 0 + BTN_H + 2, FLD_W, FLD_H);
        this.displayNameField.setMaxStringLength(32);
        //        this.displayNameField.setFocused(true);

        labelString = I18n.format("gui.radialmenu.label.keybinding");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 1, this.editsX - labelWidth / 2, PAD_TOP + OH * 1, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.changeKeyBindingBtn = this.addButton(new GuiButton(CHANGE_KEYBINDING, this.editsX - BTN_W / 2, PAD_TOP + OH * 1 + BTN_H, BTN_W, BTN_H, ""));

        labelString = I18n.format("gui.radialmenu.label.keybindingmode");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 1, this.editsX - labelWidth / 2, PAD_TOP + OH * 2, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.changeKeyModeBtn = this.addButton(new GuiButton(CHANGE_KEYBINDING_MODE, this.editsX - BTN_W / 2, PAD_TOP + OH * 2 + BTN_H, BTN_W, BTN_H, ""));

        labelString = I18n.format("gui.radialmenu.label.resourcelocation");
        labelWidth = this.fontRenderer.getStringWidth(labelString);
        label = new GuiLabel(this.fontRenderer, 2, this.editsX - labelWidth / 2, PAD_TOP + OH * 3, 0, BTN_H, 0xFFFFFFFF);
        label.addLine(labelString);
        this.labelList.add(label);

        this.iconResourceField = new GuiTextField(2, this.fontRenderer, this.editsX - FLD_W / 2, PAD_TOP + OH * 3 + BTN_H + 2, FLD_W, FLD_H);
        this.iconResourceField.setMaxStringLength(512);

        this.setButtonOptionValues(radialMenuData.get(this.selectedButton.id));*/
        this.buttonCountField.setText(Integer.toString(this.selectedButton.id));

        this.testWidget0 = new LabeledButtonWidget(this.fontRenderer);
        this.testWidget0.setBox(PANEL_W, OH, this.width - PANEL_W, PAD_TOP + OH * 0);
        ((LabelWidget) this.testWidget0.getChildren().get(0)).setText("AAAAAAAAAA");
        ((LabelWidget) this.testWidget0.getChildren().get(1)).setText("Second Label Widget A");

        this.testWidget1 = new LabeledButtonWidget(this.fontRenderer);
        this.testWidget1.setBox(PANEL_W, OH, this.width - PANEL_W, PAD_TOP + OH * 1);
        ((LabelWidget) this.testWidget1.getChildren().get(0)).setText("BBBBBBBBBB");
        ((LabelWidget) this.testWidget1.getChildren().get(1)).setText("Second Label Widget B");

        this.testWidget2 = new LabeledButtonWidget(this.fontRenderer);
        this.testWidget2.setBox(PANEL_W, OH, this.width - PANEL_W, PAD_TOP + OH * 2);
        ((LabelWidget) this.testWidget2.getChildren().get(0)).setText("CCCCCCCCCC");
        ((LabelWidget) this.testWidget2.getChildren().get(1)).setText("Second Label Widget C");

        this.testWidget3 = new LabeledButtonWidget(this.fontRenderer);
        this.testWidget3.setBox(PANEL_W, OH, this.width - PANEL_W, PAD_TOP + OH * 3);
        ((LabelWidget) this.testWidget3.getChildren().get(0)).setText("DDDDDDDDDD");
        ((LabelWidget) this.testWidget3.getChildren().get(1)).setText("Second Label Widget D");
    }

    private boolean setSelectedButton(int id) {
        for (GuiButton guiButton : buttonList) {
            if (guiButton.id != id || !(guiButton instanceof GuiRadialButton))
                continue;

            GuiRadialButton button = (GuiRadialButton) guiButton;

            this.selectedButton = button;
            button.setSelected(true);

            return true;
        }

        return false;
    }

    private void setButtonOptionValues(@NonNull RadialButtonData data) {
        this.displayNameField.setText(data.getName());

        if (data.getButtonIcon() instanceof ResourceLocation)
            this.iconResourceField.setText(data.getButtonIcon().toString());
        else
            this.iconResourceField.setText("");

        if (data.getKeyBinding() != null)
            this.changeKeyBindingBtn.displayString = I18n.format(data.getKeyBinding().getKeyDescription());
        else
            this.changeKeyBindingBtn.displayString = I18n.format("gui.radialmenu.button.unassigned");

        this.changeKeyModeBtn.displayString = data.isToggleMode() ? TOGGLE_MODE_TEXT : PRESS_MODE_TEXT;
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        if (this.reInitGui) {
            this.initGui();
            this.reInitGui = false;
        }

        this.drawDefaultBackground();

        this.testWidget0.draw(mouseX, mouseY, partialTicks);
        this.testWidget0.drawDebug();

        this.testWidget1.draw(mouseX, mouseY, partialTicks);
        this.testWidget1.drawDebug();

        this.testWidget2.draw(mouseX, mouseY, partialTicks);
        this.testWidget2.drawDebug();

        this.testWidget3.draw(mouseX, mouseY, partialTicks);
        this.testWidget3.drawDebug();

        super.drawScreen(mouseX, mouseY, partialTicks);

        this.buttonCountField.drawTextBox();
//        this.displayNameField.drawTextBox();
//        this.iconResourceField.drawTextBox();

        // Uncomment to draw debug lines
//        this.drawDebugLines();
    }

/*    private void drawDebugLines() {
        final int panelStart = this.width - PANEL_W;

        RenderHelper.drawLine(this.width - PANEL_W, PAD_TOP, this.width, PAD_TOP, this.zLevel, 0xFF00FFFF);

        for (int i = 0; i < 5; i++) {
            RenderHelper.drawLine(this.width - PANEL_W, PAD_TOP + OH * i, this.width, PAD_TOP + OH * i, this.zLevel, 0xFF00FF00); // Option boundary start
            RenderHelper.drawLine(this.width - PANEL_W, PAD_TOP + OH * i + BTN_H, this.width, PAD_TOP + OH * i + BTN_H, this.zLevel, 0xFF00FFFF); // Divide button heights
            RenderHelper.drawLine(this.width - PANEL_W, PAD_TOP + OH * i + BTN_H * 2, this.width, PAD_TOP + OH * i + BTN_H * 2, this.zLevel, 0xFFFF00FF); // Option boundary end
        }

        RenderHelper.drawLine(this.editsX, 0, this.editsX, this.height, this.zLevel, 0xFFFFFFFF);
        RenderHelper.drawLine(panelStart + PAD_LR, 0, panelStart + PAD_LR, this.height, this.zLevel, 0xFFFFFF00);
        RenderHelper.drawLine(this.width - PAD_LR, 0, this.width - PAD_LR, this.height, this.zLevel, 0xFFFFFF00);
    }*/

    @Override
    public boolean doesGuiPauseGame() {
        return true;
    }

    @Override
    protected void actionPerformed(GuiButton guiButton) {
        if (guiButton instanceof GuiRadialButton) {
            GuiRadialButton button = (GuiRadialButton) guiButton;

            if (ConfigHandler.SOUND.isButtonSoundEnabled())
                mc.getSoundHandler().playSound(PositionedSoundRecord.getMasterRecord(SoundEvents.UI_BUTTON_CLICK, 1.0F));

            button.setSelected(true);
            this.setSelectedButton(button.id);
            this.buttonCountField.setText(Integer.toString(button.id));

            for (GuiButton guiButton1 : this.buttonList)
                if ((guiButton1 instanceof GuiRadialButton) && !guiButton.equals(guiButton1))
                    ((GuiRadialButton) guiButton1).setSelected(false);

//            this.setButtonOptionValues(radialMenuData.get(button.id));
        } else {
            guiButton.playPressSound(this.mc.getSoundHandler());

            this.selectedButton = this.getSelectedButton();

            switch (guiButton.id) {
                case ADD_BTN: // Should I impose hard limit?
                    this.setSelectedButton(this.selectedButton.id + 1);
                    radialMenuData.add(this.selectedButton.id, new RadialButtonData(null, null, false, null));
                    this.buttonCountField.setText(Integer.toString(this.selectedButton.id));
                    this.reInitGui = true;
                    break;
                case DEL_BTN:
                    if (radialMenuData.size() <= 4)
                        break;

                    radialMenuData.remove(this.selectedButton.id);
                    this.buttonCountField.setText(Integer.toString(this.selectedButton.id));
                    this.setSelectedButton(this.selectedButton.id - 1);
                    this.reInitGui = true;
                    break;
                case MOVE_CCW_BTN:
                    if (this.selectedButton.id - 1 < 0) {
                        Collections.swap(radialMenuData, this.selectedButton.id, radialMenuData.size() - 1);
                        this.setSelectedButton(radialMenuData.size() - 1);
                    } else {
                        Collections.swap(radialMenuData, this.selectedButton.id, this.selectedButton.id - 1);
                        this.setSelectedButton(this.selectedButton.id - 1);
                    }

                    this.buttonCountField.setText(Integer.toString(this.selectedButton.id));
                    this.reInitGui = true;
                    break;
                case MOVE_CW_BTN:
                    if (this.selectedButton.id + 1 > radialMenuData.size() - 1) {
                        Collections.swap(radialMenuData, this.selectedButton.id, 0);
                        this.setSelectedButton(0);
                    } else {
                        Collections.swap(radialMenuData, this.selectedButton.id, this.selectedButton.id + 1);
                        this.setSelectedButton(this.selectedButton.id + 1);
                    }

                    this.buttonCountField.setText(Integer.toString(this.selectedButton.id));
                    this.reInitGui = true;
                    break;
                case CHANGE_KEYBINDING:
                    GuiControlSelect guiControlSelect = new GuiControlSelect(mc, this, result -> {
                        KeyBinding binding = (KeyBinding) result;
                        radialMenuData.get(this.selectedButton.id).setKeyBinding(binding);
                        this.reInitGui = true;
                    });
                    mc.displayGuiScreen(guiControlSelect);
                    break;
                case CHANGE_KEYBINDING_MODE: // Assign displayString directly to avoid reInitGui
                    radialMenuData.get(this.selectedButton.id).setToggleMode(!radialMenuData.get(this.selectedButton.id).isToggleMode());
//                    this.changeKeyModeBtn.displayString = radialMenuData.get(this.selectedButton.id).isToggleMode() ? TOGGLE_MODE_TEXT : PRESS_MODE_TEXT;
                    break;
            }
        }
    }

    @Override
    public void updateScreen() {
//        this.displayNameField.updateCursorCounter();
//        this.iconResourceField.updateCursorCounter();
    }

    @Override
    protected void keyTyped(char typedChar, int keyCode) {
        /*this.displayNameField.textboxKeyTyped(typedChar, keyCode);
        this.iconResourceField.textboxKeyTyped(typedChar, keyCode);

        if (keyCode == Keyboard.KEY_TAB) {
            this.displayNameField.setFocused(!this.displayNameField.isFocused());
            this.iconResourceField.setFocused(!this.iconResourceField.isFocused());
        }

        GuiRadialButton button = (GuiRadialButton) this.selectedButton;

        if (this.displayNameField.isFocused()) {
            button.displayString = this.displayNameField.getText();
            radialMenuData.get(this.selectedButton.id).setName(button.displayString);
        }

        if (this.iconResourceField.isFocused()) {
            if (this.iconResourceField.getText().isEmpty()) {
                button.imageIcon = null;
                radialMenuData.get(this.selectedButton.id).setButtonIcon(null);
            } else {
                button.imageIcon = new ResourceLocation(this.iconResourceField.getText());
                radialMenuData.get(this.selectedButton.id).setButtonIcon(button.imageIcon);
            }
        }*/
    }

    @Override
    protected void mouseClicked(int mouseX, int mouseY, int mouseButton) {
        super.mouseClicked(mouseX, mouseY, mouseButton);

//        this.displayNameField.mouseClicked(mouseX, mouseY, mouseButton);
//        this.iconResourceField.mouseClicked(mouseX, mouseY, mouseButton);
    }

    @Override
    public void drawWorldBackground(int tint) {
        if (this.mc.world != null) {
            this.drawGradientRect(0, 0, this.width - PANEL_W, this.height, 0xAA222222, 0xAA222222);
            this.drawGradientRect(this.width - PANEL_W, 0, this.width, this.height, 0xCC000000, 0xCC000000);
//            this.drawBackground(this.width - PANEL_W, 0, this.width, this.height, tint);
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
