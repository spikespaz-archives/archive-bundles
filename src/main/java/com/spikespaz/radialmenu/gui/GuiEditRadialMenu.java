package com.spikespaz.radialmenu.gui;

import com.spikespaz.radialmenu.ConfigHandler;
import com.spikespaz.radialmenu.RadialButtonData;
import com.spikespaz.radialmenu.gui.widgets.*;
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

import java.io.IOException;
import java.util.Collections;
import java.util.EnumSet;

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
    private static final int PAD_V = 8;
    private static final int PAD_H = 4;
    private static final int PAD_LR = 8;
    private static final int PAD_CTRLS = 4;
    private static final int OH = BTN_H * 2;
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
    private ButtonOptionsList buttonOptionsEditor;
    private SelectionControlsWidget controlsWidget;

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

        this.buttonOptionsEditor = new ButtonOptionsList(this.mc);
        this.buttonOptionsEditor.setBox(PANEL_W - PAD_H * 2, this.height - PAD_V * 3 - BTN_H, this.width - PANEL_W + PAD_H, PAD_V);
        this.buttonOptionsEditor.setChildHeight(OH);

        this.controlsWidget = new SelectionControlsWidget(this.mc);
        this.controlsWidget.setBox(PANEL_W, BTN_H, this.width - PANEL_W, this.height - BTN_H - PAD_V);
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

        this.buttonOptionsEditor.draw(mouseX, mouseY, partialTicks);
        this.buttonOptionsEditor.drawDebug(true);

        this.controlsWidget.draw(mouseX, mouseY, partialTicks);
        this.controlsWidget.drawDebug();

        super.drawScreen(mouseX, mouseY, partialTicks);
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
    public void drawWorldBackground(int tint) {
        if (this.mc.world != null) {
            this.drawGradientRect(0, 0, this.width - PANEL_W, this.height, 0xAA222222, 0xAA222222);
            this.drawGradientRect(this.width - PANEL_W, 0, this.width, this.height, 0xCC000000, 0xCC000000);
//            this.drawBackground(this.width - PANEL_W, 0, this.width, this.height, tint);
        } else {
            this.drawBackground(0, 0, this.width, this.height, tint);
        }
    }

    @Override
    public void handleMouseInput() throws IOException {
        super.handleMouseInput();
        this.buttonOptionsEditor.handleMouseInput();
    }

    @Override
    public void handleKeyboardInput() throws IOException {
        super.handleKeyboardInput();
        this.buttonOptionsEditor.handleKeyboardInput();
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

    @Override
    public boolean doesGuiPauseGame() {
        return true;
    }

    public class ButtonOptionsList extends ListWidget {
        protected ContainerWidget testWidget0;
        protected ContainerWidget testWidget1;
        protected ContainerWidget testWidget2;
        protected ContainerWidget testWidget3;
        protected ContainerWidget testWidget4;
        protected ContainerWidget testWidget5;

        public ButtonOptionsList(Minecraft mc) {
            super(mc);

            this.testWidget0 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget0.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget0.getChildren().get(0)).setText("AAAAAAAAAA");
            ((ButtonWidget) this.testWidget0.getChildren().get(1)).getLabelWidget().setText("Second Label Widget A");

            this.testWidget1 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget1.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget1.getChildren().get(0)).setText("BBBBBBBBBB");
            ((ButtonWidget) this.testWidget1.getChildren().get(1)).getLabelWidget().setText("Second Label Widget B");

            this.testWidget2 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget2.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget2.getChildren().get(0)).setText("CCCCCCCCCC");
            ((ButtonWidget) this.testWidget2.getChildren().get(1)).getLabelWidget().setText("Second Label Widget C");

            this.testWidget3 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget3.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget3.getChildren().get(0)).setText("DDDDDDDDDD");
            ((ButtonWidget) this.testWidget3.getChildren().get(1)).getLabelWidget().setText("Second Label Widget D");

            this.testWidget4 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget4.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget4.getChildren().get(0)).setText("EEEEEEEEEE");
            ((ButtonWidget) this.testWidget4.getChildren().get(1)).getLabelWidget().setText("Second Label Widget E");

            this.testWidget5 = (LabeledButtonWidget) this.addChild(new LabeledButtonWidget(this.mc, this.mc.fontRenderer));
            this.testWidget5.setSize(PANEL_W, OH);
            ((LabelWidget) this.testWidget5.getChildren().get(0)).setText("FFFFFFFFFF");
            ((ButtonWidget) this.testWidget5.getChildren().get(1)).getLabelWidget().setText("Second Label Widget F");
        }
    }

    public class SelectionControlsWidget extends ContainerWidget {
        protected final Minecraft mc;
        protected LabelWidget indexLabel;
        protected ButtonWidget moveCcwButton, moveCwButton, insertButton, removeButton;

        public SelectionControlsWidget(Minecraft mc) {
            this.mc = mc;

            this.childWidth = BTN_H;
            this.hPadding = PAD_CTRLS;
            this.align = EnumSet.of(Align.CH);

            this.moveCcwButton = (ButtonWidget) this.addChild(new ButtonWidget(this.mc, this.mc.fontRenderer));
            this.moveCcwButton.setWidth(BTN_H);
            this.moveCcwButton.getLabelWidget().setText("<");

            this.insertButton = (ButtonWidget) this.addChild(new ButtonWidget(this.mc, this.mc.fontRenderer));
            this.insertButton.setWidth(BTN_H);
            this.insertButton.getLabelWidget().setText("+");

            this.indexLabel = (LabelWidget) this.addChild(new LabelWidget(this.mc.fontRenderer));
            this.indexLabel.setWidth(BTN_H * 1.5);
            this.indexLabel.setText("0");

            this.removeButton = (ButtonWidget) this.addChild(new ButtonWidget(this.mc, this.mc.fontRenderer));
            this.removeButton.setWidth(BTN_H);
            this.removeButton.getLabelWidget().setText("-");

            this.moveCwButton = (ButtonWidget) this.addChild(new ButtonWidget(this.mc, this.mc.fontRenderer));
            this.moveCwButton.setWidth(BTN_H);
            this.moveCwButton.getLabelWidget().setText(">");
        }
    }
}
