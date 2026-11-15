import dick_wrapper
import customtkinter as CTk
wind = CTk.CTk()
colors, CTkimage, image = dick_wrapper.generator((33, 228, 87), (202, 123, 213, 0.0), 500, 300)
print(colors[0])
CTk.CTkLabel(wind, image=CTkimage, text="").pack(pady=30)
wind.mainloop()