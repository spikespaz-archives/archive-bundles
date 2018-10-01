import core.sys.windows.windows;
import core.thread: Thread;
import std.datetime: msecs;

void* worker;

enum uint WM_SPAWNWORKER = 0x052C;

extern (Windows) int enumWindowsCallback(void* hwnd, long) nothrow {
    void* handle = FindWindowExW(hwnd, null, "SHELLDLL_DefView", null);

    if (handle !is null)
        worker = FindWindowEx(null, hwnd, "WorkerW", null);

    return true;
}

void main() {
    void* progman = FindWindowW("Progman", null);

    uint result;
    SendMessageTimeoutW(progman, WM_SPAWNWORKER, 0, 0, SMTO_NORMAL, 1000, &result);

    EnumWindows(&enumWindowsCallback, 0);

    HDC desktop;

    while (true) {
        if (worker && !desktop)
            desktop = GetDC(worker);

        desktop.BeginPath();
        desktop.EndPath();
        desktop.Arc(10, 10, 210, 210, 110, 10, 110, 10);
        Thread.sleep(msecs(16));
    }
}
