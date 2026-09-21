import io
import qrcode
import streamlit as st
import zxingcpp
from PIL import Image


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PragyanAI - QR Code Generator & Decoder",
    page_icon="🔳",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("PragyanAI- QR Code Generator & Decoder")

st.write(
    "Generate a QR Code from a URL or information, "
    "display it, download it, and decode it."
)

st.info(
    "Built with Python + Streamlit + Pillow + QRCode + ZXing-C++. "
    "OpenCV is not used."
)


# ============================================================
# SESSION STATE
# ============================================================

if "qr_bytes" not in st.session_state:
    st.session_state.qr_bytes = None

if "generated_data" not in st.session_state:
    st.session_state.generated_data = ""


# ============================================================
# SECTION 1 — GENERATE QR CODE
# ============================================================

st.header("1️. Generate QR Code")

data = st.text_area(
    "Enter URL / Information",
    placeholder=(
        "Example:\n"
        "https://www.pragyanai.com\n\n"
        "or any text/information"
    ),
    height=120
)
# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    " Generate QR Code",
    type="primary",
    use_container_width=True
):

    if not data.strip():

        st.warning(
            "⚠️ Please enter a URL or information first."
        )

    else:

        try:

            # Create QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )

            # Add user data
            qr.add_data(data.strip())

            # Generate QR
            qr.make(fit=True)

            # Create Pillow Image
            qr_image = qr.make_image(
                fill_color="black",
                back_color="white"
            ).convert("RGB")

            # Convert image to bytes
            buffer = io.BytesIO()

            qr_image.save(
                buffer,
                format="PNG"
            )

            qr_bytes = buffer.getvalue()

            # Store in Streamlit Session State
            st.session_state.qr_bytes = qr_bytes
            st.session_state.generated_data = data.strip()

            st.success(
                "✅ QR Code generated successfully!"
            )

        except Exception as e:

            st.error(
                f"❌ Error generating QR Code: {e}"
            )
# ============================================================
# DISPLAY GENERATED QR CODE
# ============================================================

if st.session_state.qr_bytes:

    st.divider()

    st.header("2️. Generated QR Code")

    # Display QR Code
    st.image(
        st.session_state.qr_bytes,
        caption="Scan this QR Code",
        width=350
    )

    # Download QR Code
    st.download_button(
        label=" Download QR Code",
        data=st.session_state.qr_bytes,
        file_name="generated_qr_code.png",
        mime="image/png",
        use_container_width=True
    )

    # Display original data
    st.caption("Original Information")

    st.code(
        st.session_state.generated_data,
        language="text"
    )
# ============================================================
# SECTION 3 — DECODE GENERATED QR CODE
# ============================================================

st.divider()

st.header("3️. Decode Generated QR Code")

if st.button(
    " Decode QR Code",
    use_container_width=True
):

    if not st.session_state.qr_bytes:

        st.warning(
            "⚠️ Please generate a QR Code first."
        )

    else:

        try:

            # Convert bytes back to Pillow Image
            qr_image = Image.open(
                io.BytesIO(
                    st.session_state.qr_bytes
                )
            ).convert("RGB")

            # Decode QR using ZXing-C++
            results = zxingcpp.read_barcodes(
                qr_image
            )

            if results:

                decoded_data = results[0].text

                st.success(
                    "✅ QR Code decoded successfully!"
                )

                st.subheader(
                    " Decoded URL / Information"
                )

                st.code(
                    decoded_data,
                    language="text"
                )

                # If decoded content is a URL
                if decoded_data.startswith(
                    ("http://", "https://")
                ):

                    st.markdown(
                        f"###  Open Link"
                    )

                    st.markdown(
                        f"[{decoded_data}]({decoded_data})"
                    )

            else:

                st.error(
                    "❌ Could not decode the QR Code."
                )

        except Exception as e:

            st.error(
                f"❌ Error decoding QR Code: {e}"
            )
# ============================================================
# SECTION 4 — UPLOAD & DECODE EXISTING QR CODE
# ============================================================

st.divider()

st.header("4️. Decode Existing QR Code")

st.write(
    "Upload an existing QR Code image and decode "
    "the information stored inside it."
)

uploaded_file = st.file_uploader(
    "Upload QR Code Image",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)

# ============================================================
# DISPLAY UPLOADED IMAGE
# ============================================================

if uploaded_file:

    try:

        # Open uploaded image using Pillow
        uploaded_image = Image.open(
            uploaded_file
        ).convert("RGB")

        st.image(
            uploaded_image,
            caption="Uploaded QR Code",
            width=350
        )

        # Decode uploaded QR button
        if st.button(
            " Decode Uploaded QR Code",
            use_container_width=True
        ):

            results = zxingcpp.read_barcodes(
                uploaded_image
            )

            if results:

                decoded_data = results[0].text

                st.success(
                    "✅ QR Code decoded successfully!"
                )

                st.subheader(
                    " Decoded Information"
                )

                st.code(
                    decoded_data,
                    language="text"
                )

                # Display clickable URL
                if decoded_data.startswith(
                    ("http://", "https://")
                ):

                    st.markdown(
                        "###  Open Link"
                    )

                    st.markdown(
                        f"[{decoded_data}]({decoded_data})"
                    )

            else:

                st.error(
                    "❌ No QR Code detected in the uploaded image."
                )

    except Exception as e:

        st.error(
            f"❌ Error processing uploaded image: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PragyanAI | Python + Streamlit + Pillow + QRCode + ZXing-C++"
)
