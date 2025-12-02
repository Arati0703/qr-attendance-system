import streamlit as st
from datetime import datetime
import pandas as pd
from qr_utils import generate_qr, decode_qr, pil_to_bytes
from PIL import Image
import io

st.set_page_config(page_title="QR Attendance System")

st.title("🎓 QR Code Attendance System")

tab1, tab2, tab3 = st.tabs(["Generate QR", "Mark Attendance", "View Attendance"])

# ------------------ QR GENERATION -------------------
with tab1:
    st.header("Generate Student QR Code")

    name = st.text_input("Student Name")
    sid = st.text_input("Student ID")

    if st.button("Generate QR Code"):
        if name and sid:
            data = f"{name} | {sid}"
            qr_img = generate_qr(data)

            # Convert PIL → Bytes → Display
            qr_bytes = pil_to_bytes(qr_img)
            st.image(qr_bytes, caption="Your QR Code")

            st.download_button(
                "Download QR",
                data=qr_bytes,
                file_name=f"{sid}_qr.png",
                mime="image/png"
            )
        else:
            st.error("Please enter both name and student ID.")


# ------------------ MARK ATTENDANCE -------------------
with tab2:
    st.header("Upload QR Image to Mark Attendance")

    uploaded = st.file_uploader("Upload QR", type=["png", "jpg", "jpeg"])

    if uploaded:
        st.image(uploaded, caption="Uploaded QR Image")

        decoded = decode_qr(uploaded)
        if decoded:
            st.success(f"QR Content: {decoded}")

            # Extract data
            name, sid = decoded.split("|")
            name = name.strip()
            sid = sid.strip()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([[name, sid, timestamp]],
                                   columns=["Name", "Student ID", "Time"])

            # Append to CSV
            try:
                old = pd.read_csv("attendance.csv")
                df = pd.concat([old, new_row], ignore_index=True)
            except:
                df = new_row

            df.to_csv("attendance.csv", index=False)
            st.success("Attendance Marked!")
        else:
            st.error("QR could not be decoded. Try a clearer image.")


# ------------------ VIEW ATTENDANCE -------------------
with tab3:
    st.header("Attendance Records")

    try:
        data = pd.read_csv("attendance.csv")
        st.dataframe(data)
    except:
        st.info("No attendance entries found yet.")
