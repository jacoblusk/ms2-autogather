import ctypes
import signal
import sys

WINDOW_NAME = "MapleStory2 - A New Beginning"

TRUE = 1
FALSE = 0
WH_KEYBOARD_LL = 13
WM_KEYUP = 0x0101
VK_F10 = 0x79
INPUT_KEYBOARD = 1
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002
WM_QUIT = 0x0012
DIK_SPACE = 0x39

WORD = ctypes.c_ushort
DWORD = ctypes.c_ulong
UINT = ctypes.c_uint
BOOL = ctypes.c_int
HANDLE = ctypes.c_void_p
HMODULE = HANDLE
HWND = HANDLE
HINSTANCE = HANDLE
HHOOK = HANDLE
ULONG_PTR = ctypes.POINTER(ctypes.c_ulong)
LONG_PTR = ctypes.POINTER(ctypes.c_long)
UINT_PTR = ctypes.POINTER(ctypes.c_uint)
LONG = ctypes.c_long
LPSTR = ctypes.c_char_p
LRESULT = LONG_PTR
WPARAM = UINT_PTR
LPARAM = LONG_PTR
SIZE_T = ULONG_PTR
LPVOID = ctypes.c_void_p

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, WPARAM, LPARAM)
WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(DWORD, LPVOID)

class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", LPVOID),
        ("bInheritHandle", BOOL)
    ]

LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)

class POINT(ctypes.Structure):
    _fields_ = [
        ("x", LONG),
        ("y", LONG)
    ]

class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
        ("lPrivate", DWORD)
    ]

LPMSG = ctypes.POINTER(MSG)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", DWORD),
        ("scanCode", DWORD),
        ("flags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

LPKBDLLHOOKSTRUCT = ctypes.POINTER(KBDLLHOOKSTRUCT)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", DWORD),
        ("wParamL", WORD),
        ("wParamH", WORD)
    ]

class INPUT_DUMMYUNIONNAME(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", DWORD),
        ("u", INPUT_DUMMYUNIONNAME)
    ]

SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [UINT, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = UINT

SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
SetForegroundWindow.argtypes = [HWND]
SetForegroundWindow.restype = BOOL

GetWindowTextLengthA = ctypes.windll.user32.GetWindowTextLengthA
GetWindowTextLengthA.argtypes = [HWND]
GetWindowTextLengthA.restype = ctypes.c_int

GetWindowTextA = ctypes.windll.user32.GetWindowTextA
GetWindowTextA.argtypes = [HWND, LPSTR, ctypes.c_uint]
GetWindowTextA.restype = ctypes.c_int

GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = [LPSTR]
GetModuleHandleA.restype = HMODULE

SetWindowsHookExA = ctypes.windll.user32.SetWindowsHookExA
SetWindowsHookExA.argtypes = [ctypes.c_int, HOOKPROC, HINSTANCE, DWORD]
SetWindowsHookExA.restype = HHOOK

GetMessageA = ctypes.windll.user32.GetMessageA
GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessageA.restype = BOOL

TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.argtypes = [LPMSG]
TranslateMessage.restype = BOOL

DispatchMessageA = ctypes.windll.user32.DispatchMessageA
DispatchMessageA.argtypes = [LPMSG]
DispatchMessageA.restype = LRESULT

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
EnumWindows.restype = BOOL

CallNextHookEx = ctypes.windll.user32.CallNextHookEx
CallNextHookEx.argtypes = [HHOOK, ctypes.c_int, WPARAM, LPARAM]
CallNextHookEx.restype = LRESULT

IsWindowVisible = ctypes.windll.user32.IsWindowVisible
IsWindowVisible.argtypes = [HWND]
IsWindowVisible.restype = BOOL

CreateThread = ctypes.windll.kernel32.CreateThread
CreateThread.argtypes = [LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE,
                         LPVOID, DWORD, LPVOID]
CreateThread.restype = HANDLE

CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx
UnhookWindowsHookEx.argtypes = [HHOOK]
UnhookWindowsHookEx.restype = BOOL

PostQuitMessage = ctypes.windll.user32.PostQuitMessage
PostQuitMessage.argtypes = [ctypes.c_int]
PostQuitMessage.restype = None

Sleep = ctypes.windll.kernel32.Sleep
Sleep.argtypes = [DWORD]
Sleep.restype = None

g_hhook = HANDLE()
g_thread_handles = []
g_toggle = False

def close_thread_handles():
    global g_thread_handles
    for handle in g_thread_handles:
        CloseHandle(handle)
        g_thread_handles.remove(handle)

def quit():
    UnhookWindowsHookEx(g_hhook)
    close_thread_handles()
    PostQuitMessage(0)

def sigint_handler(signal, frame):
    quit()

signal.signal(signal.SIGINT, sigint_handler)

def enum_window_proc(hwnd, l_param):
    text_length = GetWindowTextLengthA(hwnd)
    buffer = ctypes.create_string_buffer(text_length + 1)
    GetWindowTextA(hwnd, buffer, text_length + 1)
    if IsWindowVisible(hwnd) and text_length > 0:
        try:
            if buffer.value.decode() == WINDOW_NAME:
                l_param[0] = hwnd
        except UnicodeDecodeError:
            pass

    return TRUE

enum_window_proc = WNDENUMPROC(enum_window_proc)

def start_routine(lp_parameter):
    while g_toggle:
        inputs = (INPUT * 2)()
        hwnd = ctypes.cast(lp_parameter, HWND)

        SetForegroundWindow(hwnd.value)
        Sleep(55)

        inputs[0].type = INPUT_KEYBOARD
        inputs[0].ki.dwFlags = KEYEVENTF_SCANCODE
        
        inputs[1] = inputs[0]
        inputs[1].ki.dwFlags = inputs[1].ki.dwFlags | KEYEVENTF_KEYUP
        inputs[0].ki.wScan = inputs[1].ki.wScan = DIK_SPACE

        SendInput(1, ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
        Sleep(55)
        SendInput(1, ctypes.byref(inputs[1]), ctypes.sizeof(INPUT))
    
    return 0

thread_proc = LPTHREAD_START_ROUTINE(start_routine)

def low_level_keyboard_proc(code, w_param, l_param):
    global g_toggle
    global g_thread_handles
    p_keyboard = ctypes.cast(l_param, LPKBDLLHOOKSTRUCT)
    w_param_value = ctypes.cast(w_param, LPVOID).value

    if w_param_value == WM_KEYUP:
        if p_keyboard[0].vkCode == VK_F10:
            g_toggle = not g_toggle

            hwnd = ctypes.c_long(0)
            EnumWindows(enum_window_proc, ctypes.byref(hwnd))
            if hwnd.value != 0 and g_toggle:
                hwnd = ctypes.cast(hwnd.value, HANDLE)
                g_thread_handles.append(
                    CreateThread(None, None, thread_proc, hwnd, 0, None))
            elif not g_toggle:
                close_thread_handles()

    lresult = CallNextHookEx(None, code, w_param, l_param)
    lresult_value = ctypes.cast(lresult, LPVOID).value
    return 0 if lresult_value == None else lresult

hook_proc = HOOKPROC(low_level_keyboard_proc)

if __name__ == "__main__":
    h_instance = GetModuleHandleA(None)
    g_hhook = SetWindowsHookExA(WH_KEYBOARD_LL,
                              hook_proc,
                              h_instance,
                              DWORD(0))
    
    msg = MSG()
    while GetMessageA(ctypes.byref(msg), None, 0, 0):
        TranslateMessage(ctypes.byref(msg))
        DispatchMessageA(ctypes.byref(msg))
    