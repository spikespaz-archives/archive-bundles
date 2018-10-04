import core.sys.windows.windows;
import core.thread: Thread;
import std.datetime: msecs;

/// Undocumented Windows message code that creates a new worker.
enum uint WM_SPAWNWORKER = 0x052C;

/// Get the framerate of the display device.
int queryFramerate() {
    DEVMODE deviceMode;
    deviceMode.dmSize = DEVMODE.sizeof;

    EnumDisplaySettingsW(null, ENUM_CURRENT_SETTINGS, &deviceMode);

    return deviceMode.dmDisplayFrequency;
}

/// Create a worker handle for drawing behind icons, on top of background.
void* createWorker() {
    void* progman = FindWindowW("Progman", null);
    void* worker;

    SendMessageW(progman, WM_SPAWNWORKER, 0, 0);

    EnumWindows(cast(ENUMWINDOWSPROC)(void* hWnd, long lParam) {
        void* handle = FindWindowExW(hWnd, null, "SHELLDLL_DefView", null);

        if (handle !is null)
            *(cast(void**) lParam) = FindWindowExW(null, hWnd, "WorkerW", null);

        return true;
    }, cast(long)&worker);

    return worker;
}

void main() {
    void* worker = createWorker();
    void* desktop = worker.GetDC();

    while (true) {
        desktop.Arc(10, 10, 210, 210, 110, 10, 110, 10);

        Thread.sleep(msecs(1000 / queryFramerate()));
    }
}
