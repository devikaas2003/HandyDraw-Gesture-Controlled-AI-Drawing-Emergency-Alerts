# HandyDraw: Gesture Controlled AI Drawing & Emergency Alerts

HandyDraw is an AI-powered, gesture-controlled drawing assistant. Using a webcam and Mediapipe hand tracking, you can:

- Draw on a virtual canvas using your index finger.
- Clear the canvas by showing all five fingers.
- Send an instant WhatsApp emergency message with a unique hand gesture (4 fingers up, 1 down).

This project demonstrates the power of computer vision, gesture recognition, and automation, combining creativity and safety.

## Features
- Gesture drawing
- Clear canvas
- WhatsApp emergency alerts
- Real-time preview
## Gesture Controls
| Gesture                 | Action                                |
|-------------------------|--------------------------------------|
| Index finger up         | Draw                                  |
| Fist                    | Stop drawing                          |
| 5 fingers up            | Clear canvas                          |
| 4 fingers up, 1 down    | Send WhatsApp emergency message       |
| ESC key                 | Quit program                          |

---


## Future Implementations
- Voice alerts
- Multi-hand gesture support
- Customizable brushes and shapes
- Gesture shortcuts (undo, redo, save)
- Expand emergency notifications to SMS or Email
- Mobile/web version

## Installation / Dependencies

HandyDraw requires **Python 3.10** and the following Python packages:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pyautogui
pip install pywin32

