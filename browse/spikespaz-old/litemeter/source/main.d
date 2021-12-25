import core.sys.windows.windows;
import std.datetime.stopwatch: StopWatch;
import std.datetime: Duration, nsecs;
import core.thread: Thread;
import std.stdio: writeln;

/// Undocumented Windows message code that creates a new worker.
enum uint WM_SPAWNWORKER = 0x052C;

void main() {
    const int framerate = queryFramerate(); // frames per second
    const long frametime = 1_000_000_000 / framerate; // nanoseconds
    writeln("Framerate (FPS): ", framerate, "\nFrametime (ms): ", frametime / 1_000_000.0);

    writeln("Creating worker...");
    HWND worker = createWorker();
    HDC desktop = worker.GetDC();

    writeln("Starting main loop...");

    renderLoop(&drawFrame, frametime, desktop);
}

/// Draw a new frame.
void drawFrame(HDC ctx) {
    ctx.Arc(10, 10, 210, 210, 110, 10, 110, 10);
}

/// Get the framerate of the display device.
int queryFramerate() {
    DEVMODE deviceMode;
    deviceMode.dmSize = DEVMODE.sizeof;

    EnumDisplaySettingsW(null, ENUM_CURRENT_SETTINGS, &deviceMode);

    return deviceMode.dmDisplayFrequency;
}

/// Create a worker handle for drawing behind icons, on top of background.
HWND createWorker() {
    HWND progman = FindWindowW("Progman", null);
    HDC worker;

    SendMessageW(progman, WM_SPAWNWORKER, 0, 0);

    EnumWindows(cast(ENUMWINDOWSPROC)(HWND hWnd, LPARAM lParam) {
        void* handle = FindWindowExW(hWnd, null, "SHELLDLL_DefView", null);

        if (handle !is null)
            *(cast(HWND*) lParam) = FindWindowExW(null, hWnd, "WorkerW", null);

        return true;
    }, cast(LPARAM)&worker);

    return worker;
}

/// Create a render loop to draw a frame when necessary.
void renderLoop(void function(HDC) drawFrame, const long frametime, HDC context) {
    StopWatch timer;
    Duration delta;

    while (true) {
        timer.reset();
        timer.start();

        drawFrame(context);

        timer.stop();

        delta = nsecs(frametime) - timer.peek();

        if (delta > nsecs(0))
            Thread.sleep(delta);
    }
}
