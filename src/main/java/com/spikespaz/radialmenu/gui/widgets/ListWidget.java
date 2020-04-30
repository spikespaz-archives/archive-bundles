package com.spikespaz.radialmenu.gui.widgets;

import com.spikespaz.radialmenu.MouseButton;
import lombok.Getter;
import lombok.Setter;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.ScaledResolution;
import org.lwjgl.input.Keyboard;
import org.lwjgl.input.Mouse;
import org.lwjgl.opengl.GL11;

import java.util.EnumSet;

public class ListWidget extends ContainerWidget {
    protected final Minecraft mc;
    @Getter @Setter
    protected double scrollPosY, scrollPosX;
    @Getter @Setter
    protected double scrollAmount;
    @Getter @Setter
    protected double tPadding, bPadding, lPadding, rPadding;
    private ScaledResolution scaledRes;

    public ListWidget(Minecraft mc) {
        super();
        this.mc = mc;
        this.align = EnumSet.of(Align.T);
        this.debugColor = 0x4433CCFF;
        // This appears to be a factor that works nicely by default.
        this.scrollAmount = 4;
    }

    @Override
    public Widget addChild(Widget widget) {
        return super.addChild(widget);
    }

    @Override
    public void draw(double mouseX, double mouseY, float partialTicks) {
        if (!this.visible)
            return;

        final double scaleW = this.mc.displayWidth / this.scaledRes.getScaledWidth_double();
        final double scaleH = this.mc.displayHeight / this.scaledRes.getScaledHeight_double();

        GL11.glEnable(GL11.GL_SCISSOR_TEST);
        GL11.glScissor((int) (this.x * scaleW), (int) (mc.displayHeight - (this.getBottom() * scaleH)), (int) (this.width * scaleW), (int) (this.height * scaleH));

        super.draw(mouseX, mouseY, partialTicks);

        GL11.glDisable(GL11.GL_SCISSOR_TEST);
}

    @Override
    public void update() {
        super.update();

        this.scaledRes = new ScaledResolution(this.mc);

        for (Widget child : this.children) {
            if (this.align.contains(Align.T))
                child.y -= this.scrollPosY;
            else if (this.align.contains(Align.L))
                child.x -= this.scrollPosX;

            child.setVisible(child.getRight() >= this.x && child.x <= this.getRight() && child.getBottom() >= this.y && child.y <= this.getBottom());
        }
    }

    public void drawDebug(boolean scissor) {
        if (!this.visible)
            return;

        if (scissor) {
            final double scaleW = this.mc.displayWidth / this.scaledRes.getScaledWidth_double();
            final double scaleH = this.mc.displayHeight / this.scaledRes.getScaledHeight_double();

            GL11.glEnable(GL11.GL_SCISSOR_TEST);
            GL11.glScissor((int) (this.x * scaleW), (int) (mc.displayHeight - (this.getBottom() * scaleH)), (int) (this.width * scaleW), (int) (this.height * scaleH));
        }

        super.drawDebug();

        if (scissor)
            GL11.glDisable(GL11.GL_SCISSOR_TEST);
    }

    public void handleMouseInput() {
        if (Mouse.getEventButton() == MouseButton.M) {
            System.out.println(Mouse.getEventDWheel());
            final double scroll = Mouse.getEventDWheel();

            if (scroll != 0) {
                if (Keyboard.isKeyDown(Keyboard.KEY_LCONTROL))
                    this.scrollPosX += (scroll / -120f) * this.childWidth / 2;
                else
                    this.scrollPosY += (scroll / -120f) * this.childHeight / 2;
            }
        }
    }

    public void handleKeyboardInput() {
        switch (Keyboard.getEventKey()) {
            case Keyboard.KEY_UP:
                this.scrollPosY += this.scrollAmount;
                this.scrollPosY = Math.min(this.scrollPosY, this.contentHeight - height);
                break;
            case Keyboard.KEY_DOWN:
                this.scrollPosY -= this.scrollAmount;
                this.scrollPosY = Math.max(0, this.scrollPosY);
                break;
            case Keyboard.KEY_LEFT:
                this.scrollPosX += this.scrollAmount;
                this.scrollPosX = Math.min(this.scrollPosX, this.contentWidth - width);
                break;
            case Keyboard.KEY_RIGHT:
                this.scrollPosX -= this.scrollAmount;
                this.scrollPosX = Math.max(0, this.scrollPosX);
                break;
        }
    }
}
