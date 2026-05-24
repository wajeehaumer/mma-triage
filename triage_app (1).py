"""
MMA Symptom Triage Tool — GKN Aerospace Garden Grove Incident
=============================================================
100% FREE — No API key, no credit card, no external services
Rule-based clinical triage engine (evidence: EPA, NIOSH, NCBI/IARC)
Multilingual: English / Tiếng Việt / Español
Deploy FREE on Streamlit Community Cloud

Author: Wajeeha Umer, PhD Candidate
        Environmental Health Sciences, UC Irvine · wumer@uci.edu
"""

import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MMA Triage · Garden Grove Emergency",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# FULL TRANSLATION MATRIX
# ─────────────────────────────────────────────────────────────────────────────
T = {
    "English": {
        "title":    "🏥 MMA Exposure Symptom Checker",
        "subtitle": "GKN Aerospace Garden Grove · Evidence-Based · Free Tool",
        "banner": (
            "⚠️ This tool does NOT replace a doctor. "
            "Chest pain or cannot breathe — call 911 NOW. "
            "If anything feels wrong, trust your body and go to the medical station."
        ),
        "hotlines": (
            "📞 OCFA Medical: (714) 538-2501  ·  "
            "🚨 Emergency: 911  ·  "
            "ℹ️ Info: (714) 741-5444  ·  "
            "☠️ Poison Control: 1-800-222-1222"
        ),
        "what_is_mma": "ℹ️ What is MMA? — All Proven Health Effects (EPA / NIOSH / NCBI)",
        "mma_info": (
            "**Methyl Methacrylate (MMA)** is a volatile, flammable chemical. "
            "The GKN tank contained thousands of gallons. Documented health effects:\n\n"
            "🫁 **Respiratory:** Chest tightness, shortness of breath, coughing, wheezing\n\n"
            "👁️ **Eyes/Nose/Throat:** Burning eyes, runny nose, sore throat\n\n"
            "🧠 **Neurological (proven in humans):** Headache, dizziness, "
            "lethargy, heaviness/weakness in arms and legs\n\n"
            "🩺 **Skin (often delayed hours):** MMA absorbs through skin. "
            "Causes redness, burning, and allergic contact dermatitis "
            "(blistering, eczema — Type IV reaction appearing hours later)\n\n"
            "❤️ **Cardiovascular:** Palpitations documented in occupational exposures\n\n"
            "🤢 **Gastrointestinal:** Nausea, vomiting\n\n"
            "🤰 **Pregnancy:** Fetal weight reduction in animal studies. "
            "ANY exposure → seek medical evaluation regardless of symptoms\n\n"
            "🚫 **Cancer:** EPA classifies MMA as NOT likely carcinogenic — "
            "no cancer risk from this exposure\n\n"
            "*Sources: EPA Tox Review MMA (2016), NIOSH, NCBI/IARC Vol.60, BASF SDS Oct 2025*"
        ),
        "section_who":      "👤 About You",
        "section_expo":     "🧪 Your Exposure",
        "section_symptoms": "🤒 Respiratory & Systemic Symptoms",
        "section_skin":     "🩺 Skin Symptoms",
        "age_label":  "Age group",
        "age_opts":   ["Child (0–12)", "Teen (13–17)", "Adult (18–64)", "Senior (65+)"],
        "preg_label": "Are you pregnant or possibly pregnant?",
        "preg_opts":  ["No", "Yes", "Unsure"],
        "cond_label": "Pre-existing conditions (select all that apply)",
        "cond_opts":  [
            "Asthma", "COPD / Emphysema", "Heart disease / Arrhythmia",
            "Diabetes", "Kidney disease", "Skin allergy / Eczema history",
            "None of the above"
        ],
        "expo_label":      "Were you inside the evacuation zone?",
        "expo_opts":       ["Yes — I was inside the zone", "No — I left before orders", "Unsure"],
        "duration_label":  "How long were you outdoors in the zone?",
        "duration_opts":   [
            "Less than 30 minutes", "30 min – 2 hours",
            "2–6 hours", "More than 6 hours", "I stayed indoors the whole time"
        ],
        "skin_expo_label": "Did MMA liquid or mist contact your skin or clothing?",
        "skin_expo_opts":  ["No", "Yes — skin contact", "Yes — clothing soaked/splashed", "Unsure"],
        "sym_label": "Select ALL symptoms you have RIGHT NOW:",
        "sym_opts": [
            "Eye burning, tearing, or irritation",
            "Runny nose or sneezing",
            "Sore or burning throat",
            "Coughing",
            "Wheezing",
            "Shortness of breath / difficulty breathing",
            "Chest tightness or pain",
            "Headache",
            "Dizziness or lightheadedness",
            "Lethargy / unusual fatigue",
            "Heaviness or weakness in arms or legs",
            "Heart palpitations or racing heart",
            "Nausea",
            "Vomiting",
            "No respiratory or systemic symptoms",
        ],
        "skin_sym_label": (
            "Select ALL skin symptoms "
            "(skin effects can be delayed hours — check carefully):"
        ),
        "skin_sym_opts": [
            "Skin redness or irritation at contact area",
            "Burning sensation on skin",
            "Itching or hives",
            "Blistering or oozing rash (contact dermatitis)",
            "Skin rash spreading beyond contact area",
            "Numbness or tingling in fingers / hands",
            "No skin symptoms",
        ],
        "onset_label": "When did your first symptoms appear?",
        "onset_opts":  [
            "Just now (within 1 hour)", "1–6 hours ago",
            "6–24 hours ago", "More than 24 hours ago", "No symptoms yet"
        ],
        "submit_btn":    "🔍 Check My Symptoms",
        "result_header": "📋 Your Triage Assessment",
        "disclaimer": (
            "⚠️ This assessment is for public health guidance only. "
            "It does not diagnose medical conditions and is not a substitute "
            "for professional medical advice. Always follow instructions from "
            "OCFA and OCHCA emergency personnel at your shelter."
        ),
        "share_header": "📲 Share This Tool",
        "share_text":   "Show this link to others at the shelter:",
        "powered_by": (
            "Free tool · No AI API · Rule-based clinical engine · "
            "Evidence: EPA, NIOSH, NCBI · "
            "Wajeeha Umer, PhD · EHS · UC Irvine · wumer@uci.edu"
        ),
        # ── Triage result strings ──────────────────────────────────────────
        "levels": {
            "911":     "🚨 CALL 911 NOW",
            "clinic":  "⚠️ Go to Medical Station Now",
            "monitor": "👁️ Monitor Your Symptoms",
            "ok":      "✅ You Appear Safe",
        },
        "headlines": {
            "911": (
                "Your symptoms indicate a potentially life-threatening emergency. "
                "Do not wait — call 911 or go to the medical station immediately."
            ),
            "clinic": (
                "Your symptoms or risk profile require evaluation by medical staff. "
                "Go to the medical station at this shelter now."
            ),
            "monitor": (
                "Your symptoms are mild. Rest, remove exposed clothing, "
                "wash exposed skin, and watch closely for any changes."
            ),
            "ok": (
                "No significant symptoms detected. Stay sheltered and monitor — "
                "some MMA effects appear hours later."
            ),
        },
        "todo": {
            "911": [
                "Call 911 immediately or have someone take you to the medical station",
                "Sit upright if you have difficulty breathing",
                "Tell staff you were in the MMA evacuation zone",
                "Remove and bag any clothing that may have MMA vapor or liquid",
            ],
            "clinic": [
                "Go to the medical station at this shelter RIGHT NOW",
                "Tell staff you were in the MMA zone and describe your symptoms",
                "Remove and double-bag clothing exposed to MMA vapor — shower if possible",
                "Wash any exposed skin with soap and water for 15 minutes",
                "Bring any medications you currently take",
            ],
            "monitor": [
                "Stay indoors at the shelter — avoid outdoor air",
                "Remove and bag clothing worn during exposure — shower if available",
                "Wash exposed skin with soap and water for at least 15 minutes",
                "Drink water and rest — avoid physical exertion",
                "Check back on this tool if any symptoms worsen",
            ],
            "ok": [
                "Stay inside the shelter — do NOT return to the evacuation zone",
                "If you wore clothes outside: remove, bag, and wash exposed skin as precaution",
                "Drink water and rest",
                "Monitor for any new symptoms over the next 24 hours",
                "Check official updates: ggcity.org/emergency",
            ],
        },
        "watch_for": {
            "911": [
                "Blue lips or fingertips (cyanosis)",
                "Loss of consciousness or collapse",
                "Unable to speak full sentences",
                "Vomiting that will not stop",
            ],
            "clinic": [
                "Shortness of breath worsening",
                "Chest tightness increasing",
                "Skin rash spreading or blistering",
                "Increasing confusion or limb weakness",
            ],
            "monitor": [
                "Any new shortness of breath or chest tightness",
                "Skin rash appearing hours later (delayed dermatitis)",
                "Worsening headache or dizziness",
                "Unusual limb heaviness or fatigue",
            ],
            "ok": [
                "Any new eye, nose, or throat irritation",
                "Skin rash or itching appearing (delayed reaction possible up to 24h)",
                "Headache or dizziness developing",
                "Any breathing changes",
            ],
        },
        "skin_notes": {
            "911":    "Remove and double-bag ALL clothing immediately. Wash skin with soap and water for 15 minutes.",
            "clinic": "🩺 MMA absorbs through skin. Remove all exposed clothing and double-bag it. Wash skin with soap and water for 15 min. Watch for delayed rash or blistering appearing hours later.",
            "monitor":"⚠️ MMA skin effects can be delayed 6–24 hours. Check your skin again in a few hours. Any new rash, blistering, or spreading irritation → go to the medical station immediately.",
            "ok":     "",
        },
        "reassurance": {
            "911":    "Emergency medical staff at this shelter are trained for MMA exposure. Get to them now.",
            "clinic": "Many evacuees are experiencing similar symptoms. Medical staff here are trained for MMA exposure.",
            "monitor":"Mild symptoms from brief MMA vapor exposure typically resolve with fresh air and rest. You are doing the right things.",
            "ok":     "You are safe in the shelter. Emergency crews are working around the clock. Check back if any new symptoms appear.",
        },
    },

    # ── VIETNAMESE ────────────────────────────────────────────────────────────
    "Tiếng Việt": {
        "title":    "🏥 Kiểm Tra Triệu Chứng Tiếp Xúc MMA",
        "subtitle": "GKN Aerospace Garden Grove · Dựa Trên Bằng Chứng · Miễn Phí",
        "banner": (
            "⚠️ Công cụ này KHÔNG thay thế bác sĩ. "
            "Đau ngực hoặc không thở được — GỌI 911 NGAY. "
            "Nếu cảm thấy có gì không ổn, hãy tin vào cơ thể và đến trạm y tế ngay."
        ),
        "hotlines": (
            "📞 Y tế OCFA: (714) 538-2501  ·  "
            "🚨 Khẩn cấp: 911  ·  "
            "ℹ️ Thông tin: (714) 741-5444  ·  "
            "☠️ Kiểm soát độc: 1-800-222-1222"
        ),
        "what_is_mma": "ℹ️ MMA là gì? — Tất cả tác động sức khỏe (EPA / NIOSH / NCBI)",
        "mma_info": (
            "**Methyl Methacrylate (MMA)** là hóa chất dễ bay hơi, dễ cháy. "
            "Bể chứa tại GKN chứa hàng ngàn gallon. Các tác động sức khỏe được ghi nhận:\n\n"
            "🫁 **Hô hấp:** Tức ngực, khó thở, ho, thở khò khè\n\n"
            "👁️ **Mắt/Mũi/Họng:** Bỏng mắt, chảy nước mũi, đau họng\n\n"
            "🧠 **Thần kinh (chứng minh ở người):** Đau đầu, chóng mặt, "
            "mệt mỏi bất thường, nặng nề/yếu ớt ở tay chân\n\n"
            "🩺 **Da (thường bị trì hoãn nhiều giờ):** MMA được hấp thụ qua da. "
            "Gây đỏ da, bỏng rát, và viêm da tiếp xúc dị ứng "
            "(phồng rộp, chàm — có thể xuất hiện nhiều giờ sau)\n\n"
            "❤️ **Tim mạch:** Đánh trống ngực được ghi nhận\n\n"
            "🤢 **Tiêu hóa:** Buồn nôn, nôn mửa\n\n"
            "🤰 **Thai kỳ:** Giảm cân thai nhi trong nghiên cứu động vật. "
            "BẤT KỲ mức tiếp xúc nào → cần khám y tế\n\n"
            "🚫 **Ung thư:** EPA phân loại MMA KHÔNG có khả năng gây ung thư\n\n"
            "*Nguồn: EPA, NIOSH, NCBI/IARC, BASF SDS 2025*"
        ),
        "section_who":      "👤 Thông Tin Của Bạn",
        "section_expo":     "🧪 Mức Độ Tiếp Xúc",
        "section_symptoms": "🤒 Triệu Chứng Hô Hấp & Toàn Thân",
        "section_skin":     "🩺 Triệu Chứng Da",
        "age_label":  "Nhóm tuổi",
        "age_opts":   ["Trẻ em (0–12)", "Thiếu niên (13–17)", "Người lớn (18–64)", "Người cao tuổi (65+)"],
        "preg_label": "Bạn có đang mang thai hoặc có thể mang thai?",
        "preg_opts":  ["Không", "Có", "Không chắc"],
        "cond_label": "Bệnh có sẵn (chọn tất cả)",
        "cond_opts":  [
            "Hen suyễn", "COPD / Khí thũng", "Bệnh tim / Rối loạn nhịp",
            "Tiểu đường", "Bệnh thận", "Dị ứng da / Chàm",
            "Không có"
        ],
        "expo_label":      "Bạn có ở trong vùng sơ tán không?",
        "expo_opts":       ["Có — Tôi ở trong vùng", "Không — Tôi rời trước lệnh", "Không chắc"],
        "duration_label":  "Bạn ở ngoài trời trong khu vực bao lâu?",
        "duration_opts":   [
            "Dưới 30 phút", "30 phút – 2 giờ",
            "2–6 giờ", "Hơn 6 giờ", "Tôi ở trong nhà suốt"
        ],
        "skin_expo_label": "Chất lỏng hoặc sương MMA có tiếp xúc với da hoặc quần áo của bạn không?",
        "skin_expo_opts":  ["Không", "Có — tiếp xúc da", "Có — quần áo bị thấm/văng", "Không chắc"],
        "sym_label": "Chọn TẤT CẢ triệu chứng bạn đang có NGAY BÂY GIỜ:",
        "sym_opts": [
            "Mắt bỏng rát, chảy nước mắt hoặc kích ứng",
            "Chảy nước mũi hoặc hắt hơi",
            "Đau hoặc bỏng họng",
            "Ho",
            "Thở khò khè",
            "Khó thở",
            "Tức ngực hoặc đau ngực",
            "Đau đầu",
            "Chóng mặt",
            "Mệt mỏi bất thường / uể oải",
            "Nặng nề hoặc yếu ớt ở tay chân",
            "Tim đập nhanh hoặc hồi hộp",
            "Buồn nôn",
            "Nôn mửa",
            "Không có triệu chứng hô hấp hoặc toàn thân",
        ],
        "skin_sym_label": (
            "Chọn TẤT CẢ triệu chứng da "
            "(tác động da có thể bị trì hoãn nhiều giờ — kiểm tra kỹ):"
        ),
        "skin_sym_opts": [
            "Đỏ da hoặc kích ứng ở vùng tiếp xúc",
            "Cảm giác bỏng rát trên da",
            "Ngứa hoặc nổi mề đay",
            "Phồng rộp hoặc phát ban rỉ nước (viêm da tiếp xúc)",
            "Phát ban lan ra ngoài vùng tiếp xúc",
            "Tê hoặc ngứa ran ở ngón tay / bàn tay",
            "Không có triệu chứng da",
        ],
        "onset_label": "Triệu chứng đầu tiên xuất hiện khi nào?",
        "onset_opts":  [
            "Vừa mới (trong 1 giờ)", "1–6 giờ trước",
            "6–24 giờ trước", "Hơn 24 giờ trước", "Chưa có triệu chứng"
        ],
        "submit_btn":    "🔍 Kiểm Tra Triệu Chứng",
        "result_header": "📋 Kết Quả Phân Loại",
        "disclaimer": (
            "⚠️ Đánh giá này chỉ mang tính hướng dẫn sức khỏe cộng đồng. "
            "Không chẩn đoán bệnh. Luôn tuân theo hướng dẫn của nhân viên "
            "OCFA và OCHCA tại nơi trú ẩn."
        ),
        "share_header": "📲 Chia Sẻ Công Cụ Này",
        "share_text":   "Cho người khác tại nơi trú ẩn xem đường dẫn này:",
        "powered_by": (
            "Miễn phí · Không cần AI · Dựa trên bằng chứng EPA, NIOSH, NCBI · "
            "Wajeeha Umer, PhD · EHS · UC Irvine · wumer@uci.edu"
        ),
        "levels": {
            "911":     "🚨 GỌI 911 NGAY",
            "clinic":  "⚠️ Đến Trạm Y Tế Ngay",
            "monitor": "👁️ Theo Dõi Triệu Chứng",
            "ok":      "✅ Bạn Có Vẻ An Toàn",
        },
        "headlines": {
            "911":     "Triệu chứng của bạn cho thấy tình trạng nguy hiểm đến tính mạng. Gọi 911 hoặc đến trạm y tế ngay lập tức.",
            "clinic":  "Triệu chứng hoặc yếu tố nguy cơ của bạn cần được đánh giá bởi nhân viên y tế ngay bây giờ.",
            "monitor": "Triệu chứng của bạn còn nhẹ. Nghỉ ngơi, thay quần áo, rửa da và theo dõi chặt chẽ.",
            "ok":      "Không phát hiện triệu chứng đáng kể. Tiếp tục ở lại nơi trú ẩn — một số tác động MMA có thể xuất hiện nhiều giờ sau.",
        },
        "todo": {
            "911": [
                "Gọi 911 ngay lập tức hoặc nhờ người đưa đến trạm y tế",
                "Ngồi thẳng nếu khó thở",
                "Cho nhân viên biết bạn đã ở trong vùng MMA",
                "Cởi và đóng túi quần áo có thể dính hơi hoặc chất lỏng MMA",
            ],
            "clinic": [
                "Đến trạm y tế tại nơi trú ẩn này NGAY BÂY GIỜ",
                "Cho nhân viên biết bạn đã ở vùng MMA và mô tả triệu chứng",
                "Cởi và đóng túi đôi quần áo tiếp xúc với hơi MMA — tắm nếu có thể",
                "Rửa da bằng xà phòng và nước trong 15 phút",
                "Mang theo thuốc bạn đang dùng",
            ],
            "monitor": [
                "Ở trong nơi trú ẩn — tránh không khí ngoài trời",
                "Cởi và đóng túi quần áo đã mặc khi tiếp xúc — tắm nếu có thể",
                "Rửa da bằng xà phòng và nước ít nhất 15 phút",
                "Uống nước và nghỉ ngơi — tránh vận động mạnh",
                "Kiểm tra lại công cụ này nếu triệu chứng nặng hơn",
            ],
            "ok": [
                "Ở lại trong nơi trú ẩn — KHÔNG trở về vùng sơ tán",
                "Nếu mặc quần áo ra ngoài: cởi, đóng túi và rửa da tiếp xúc",
                "Uống nước và nghỉ ngơi",
                "Theo dõi triệu chứng mới trong 24 giờ tới",
                "Theo dõi thông tin chính thức: ggcity.org/emergency",
            ],
        },
        "watch_for": {
            "911": [
                "Môi hoặc đầu ngón tay tím tái",
                "Mất ý thức hoặc ngã xuống",
                "Không nói được câu hoàn chỉnh",
                "Nôn mửa không dừng lại",
            ],
            "clinic": [
                "Khó thở ngày càng tệ hơn",
                "Tức ngực tăng lên",
                "Phát ban lan ra hoặc phồng rộp",
                "Lú lẫn hoặc yếu tay chân tăng lên",
            ],
            "monitor": [
                "Bất kỳ khó thở hoặc tức ngực mới nào",
                "Phát ban da xuất hiện nhiều giờ sau (viêm da trì hoãn)",
                "Đau đầu hoặc chóng mặt nặng hơn",
                "Mệt mỏi hoặc nặng nề ở tay chân bất thường",
            ],
            "ok": [
                "Bất kỳ kích ứng mắt, mũi hoặc họng mới nào",
                "Phát ban da hoặc ngứa xuất hiện (có thể trì hoãn đến 24h)",
                "Đau đầu hoặc chóng mặt phát triển",
                "Bất kỳ thay đổi về hô hấp nào",
            ],
        },
        "skin_notes": {
            "911":    "Cởi và đóng túi đôi TẤT CẢ quần áo ngay lập tức. Rửa da bằng xà phòng và nước trong 15 phút.",
            "clinic": "🩺 MMA được hấp thụ qua da. Cởi tất cả quần áo tiếp xúc và đóng túi đôi. Rửa da bằng xà phòng và nước 15 phút. Chú ý phát ban hoặc phồng rộp trì hoãn xuất hiện nhiều giờ sau.",
            "monitor":"⚠️ Tác động da MMA có thể bị trì hoãn 6–24 giờ. Kiểm tra da lại sau vài giờ. Bất kỳ phát ban, phồng rộp hoặc kích ứng lan ra → đến trạm y tế ngay.",
            "ok":     "",
        },
        "reassurance": {
            "911":    "Nhân viên y tế khẩn cấp tại đây được đào tạo cho tiếp xúc MMA. Đến gặp họ ngay.",
            "clinic": "Nhiều người sơ tán đang có triệu chứng tương tự. Nhân viên y tế ở đây được đào tạo cho tiếp xúc MMA.",
            "monitor":"Triệu chứng nhẹ do tiếp xúc hơi MMA ngắn hạn thường hết khi nghỉ ngơi và hít không khí trong lành.",
            "ok":     "Bạn an toàn trong nơi trú ẩn. Nhân viên cứu hộ đang làm việc ngày đêm.",
        },
    },

    # ── SPANISH ───────────────────────────────────────────────────────────────
    "Español": {
        "title":    "🏥 Verificador de Síntomas de Exposición a MMA",
        "subtitle": "GKN Aerospace Garden Grove · Basado en Evidencia · Herramienta Gratuita",
        "banner": (
            "⚠️ Esta herramienta NO reemplaza a un médico. "
            "Dolor en el pecho o no puede respirar — llame al 911 AHORA. "
            "Si algo se siente mal, confíe en su cuerpo y vaya a la estación médica."
        ),
        "hotlines": (
            "📞 Médico OCFA: (714) 538-2501  ·  "
            "🚨 Emergencias: 911  ·  "
            "ℹ️ Info: (714) 741-5444  ·  "
            "☠️ Control de venenos: 1-800-222-1222"
        ),
        "what_is_mma": "ℹ️ ¿Qué es el MMA? — Todos los efectos en salud (EPA / NIOSH / NCBI)",
        "mma_info": (
            "**El Metacrilato de Metilo (MMA)** es un químico volátil e inflamable. "
            "El tanque de GKN contenía miles de galones. Efectos documentados:\n\n"
            "🫁 **Respiratorios:** Opresión, dificultad para respirar, tos, sibilancias\n\n"
            "👁️ **Ojos/Nariz/Garganta:** Ardor ocular, secreción nasal, dolor de garganta\n\n"
            "🧠 **Neurológicos (probados en humanos):** Dolor de cabeza, mareos, "
            "letargo, pesadez/debilidad en brazos y piernas\n\n"
            "🩺 **Piel (frecuentemente tardío — horas después):** El MMA se absorbe "
            "por la piel. Causa enrojecimiento, ardor y dermatitis de contacto "
            "alérgica (ampollas, eccema — reacción tipo IV que aparece horas después)\n\n"
            "❤️ **Cardiovasculares:** Palpitaciones documentadas en exposiciones\n\n"
            "🤢 **Gastrointestinales:** Náuseas, vómitos\n\n"
            "🤰 **Embarazo:** Reducción del peso fetal en estudios animales. "
            "CUALQUIER exposición → busque evaluación médica\n\n"
            "🚫 **Cáncer:** EPA clasifica el MMA como NO probable carcinógeno\n\n"
            "*Fuentes: EPA, NIOSH, NCBI/IARC, BASF SDS Oct 2025*"
        ),
        "section_who":      "👤 Información Personal",
        "section_expo":     "🧪 Su Exposición",
        "section_symptoms": "🤒 Síntomas Respiratorios y Sistémicos",
        "section_skin":     "🩺 Síntomas de Piel",
        "age_label":  "Grupo de edad",
        "age_opts":   ["Niño (0–12)", "Adolescente (13–17)", "Adulto (18–64)", "Mayor (65+)"],
        "preg_label": "¿Está embarazada o podría estarlo?",
        "preg_opts":  ["No", "Sí", "No estoy segura"],
        "cond_label": "Condiciones previas (marque todas las que apliquen)",
        "cond_opts":  [
            "Asma", "EPOC / Enfisema", "Enfermedad cardíaca / Arritmia",
            "Diabetes", "Enfermedad renal", "Alergia de piel / Eccema",
            "Ninguna"
        ],
        "expo_label":      "¿Estaba en la zona de evacuación?",
        "expo_opts":       ["Sí — estaba dentro de la zona", "No — salí antes de las órdenes", "No estoy seguro/a"],
        "duration_label":  "¿Cuánto tiempo estuvo al aire libre en la zona?",
        "duration_opts":   [
            "Menos de 30 minutos", "30 min – 2 horas",
            "2–6 horas", "Más de 6 horas", "Permanecí adentro todo el tiempo"
        ],
        "skin_expo_label": "¿El líquido o niebla de MMA entró en contacto con su piel o ropa?",
        "skin_expo_opts":  ["No", "Sí — contacto con piel", "Sí — ropa empapada/salpicada", "No estoy seguro/a"],
        "sym_label": "Seleccione TODOS los síntomas que tiene AHORA MISMO:",
        "sym_opts": [
            "Ardor, lagrimeo o irritación en los ojos",
            "Secreción nasal o estornudos",
            "Dolor o ardor de garganta",
            "Tos",
            "Sibilancias (silbidos al respirar)",
            "Dificultad para respirar",
            "Opresión o dolor en el pecho",
            "Dolor de cabeza",
            "Mareos o sensación de desmayo",
            "Letargo / fatiga inusual",
            "Pesadez o debilidad en brazos o piernas",
            "Palpitaciones o corazón acelerado",
            "Náuseas",
            "Vómitos",
            "Sin síntomas respiratorios o sistémicos",
        ],
        "skin_sym_label": (
            "Seleccione TODOS los síntomas de piel "
            "(los efectos cutáneos pueden retrasarse horas — revise con cuidado):"
        ),
        "skin_sym_opts": [
            "Enrojecimiento o irritación en el área de contacto",
            "Sensación de ardor en la piel",
            "Picazón o ronchas",
            "Ampollas o sarpullido con secreción (dermatitis de contacto)",
            "Sarpullido que se extiende más allá del contacto",
            "Entumecimiento u hormigueo en dedos / manos",
            "Sin síntomas de piel",
        ],
        "onset_label": "¿Cuándo aparecieron sus primeros síntomas?",
        "onset_opts":  [
            "Ahora mismo (última hora)", "Hace 1–6 horas",
            "Hace 6–24 horas", "Hace más de 24 horas", "Aún sin síntomas"
        ],
        "submit_btn":    "🔍 Evaluar Mis Síntomas",
        "result_header": "📋 Su Evaluación de Triaje",
        "disclaimer": (
            "⚠️ Esta evaluación es solo orientación de salud pública. "
            "No diagnostica enfermedades. Siga siempre las instrucciones "
            "del personal de OCFA y OCHCA en su refugio."
        ),
        "share_header": "📲 Comparta Esta Herramienta",
        "share_text":   "Muestre este enlace a otros en el refugio:",
        "powered_by": (
            "Herramienta gratuita · Sin IA · Motor clínico basado en reglas · "
            "Evidencia: EPA, NIOSH, NCBI · "
            "Wajeeha Umer, PhD · EHS · UC Irvine · wumer@uci.edu"
        ),
        "levels": {
            "911":     "🚨 LLAME AL 911 AHORA",
            "clinic":  "⚠️ Vaya a la Estación Médica Ahora",
            "monitor": "👁️ Monitoree Sus Síntomas",
            "ok":      "✅ Parece Estar Seguro/a",
        },
        "headlines": {
            "911":     "Sus síntomas indican una emergencia potencialmente mortal. No espere — llame al 911 o vaya a la estación médica de inmediato.",
            "clinic":  "Sus síntomas o perfil de riesgo requieren evaluación médica. Vaya a la estación médica de este refugio ahora.",
            "monitor": "Sus síntomas son leves. Descanse, cambie de ropa, lave la piel expuesta y observe de cerca.",
            "ok":      "No se detectaron síntomas significativos. Permanezca en el refugio — algunos efectos del MMA aparecen horas después.",
        },
        "todo": {
            "911": [
                "Llame al 911 inmediatamente o pida que lo lleven a la estación médica",
                "Siéntese erguido si tiene dificultad para respirar",
                "Diga al personal que estuvo en la zona de evacuación MMA",
                "Retire y embolse la ropa que pueda tener vapor o líquido MMA",
            ],
            "clinic": [
                "Vaya a la estación médica de este refugio AHORA MISMO",
                "Diga al personal que estuvo en la zona MMA y describa sus síntomas",
                "Retire y doble bolse la ropa expuesta — dúchese si es posible",
                "Lave la piel expuesta con agua y jabón durante 15 minutos",
                "Traiga los medicamentos que toma actualmente",
            ],
            "monitor": [
                "Permanezca adentro en el refugio — evite el aire exterior",
                "Retire y embolse la ropa usada durante la exposición — dúchese si está disponible",
                "Lave la piel expuesta con agua y jabón al menos 15 minutos",
                "Beba agua y descanse — evite el esfuerzo físico",
                "Consulte esta herramienta si algún síntoma empeora",
            ],
            "ok": [
                "Permanezca en el refugio — NO regrese a la zona de evacuación",
                "Si usó ropa afuera: retírela, embolsela y lave la piel expuesta",
                "Beba agua y descanse",
                "Monitoree síntomas nuevos durante las próximas 24 horas",
                "Consulte actualizaciones: ggcity.org/emergency",
            ],
        },
        "watch_for": {
            "911": [
                "Labios o dedos azules (cianosis)",
                "Pérdida del conocimiento o colapso",
                "Incapaz de hablar en oraciones completas",
                "Vómitos que no cesan",
            ],
            "clinic": [
                "Dificultad para respirar que empeora",
                "Opresión en el pecho que aumenta",
                "Sarpullido que se extiende o forma ampollas",
                "Confusión o debilidad en extremidades que empeora",
            ],
            "monitor": [
                "Cualquier dificultad para respirar o presión en el pecho nueva",
                "Sarpullido que aparece horas después (dermatitis tardía)",
                "Dolor de cabeza o mareos que empeoran",
                "Fatiga o pesadez inusual en extremidades",
            ],
            "ok": [
                "Cualquier irritación nueva de ojos, nariz o garganta",
                "Sarpullido o picazón que aparece (reacción tardía posible hasta 24h)",
                "Dolor de cabeza o mareos que se desarrollan",
                "Cualquier cambio en la respiración",
            ],
        },
        "skin_notes": {
            "911":    "Retire y doble bolse TODA la ropa inmediatamente. Lave la piel con agua y jabón durante 15 minutos.",
            "clinic": "🩺 El MMA se absorbe por la piel. Retire toda la ropa expuesta y doble bolsela. Lave la piel con agua y jabón 15 min. Observe sarpullido o ampollas tardías que aparecen horas después.",
            "monitor":"⚠️ Los efectos cutáneos del MMA pueden retrasarse 6–24 horas. Revise su piel nuevamente en unas horas. Cualquier sarpullido, ampolla o irritación que se extienda → vaya a la estación médica.",
            "ok":     "",
        },
        "reassurance": {
            "911":    "El personal médico de emergencia aquí está capacitado para la exposición a MMA. Vaya a ellos ahora.",
            "clinic": "Muchos evacuados experimentan síntomas similares. El personal médico aquí está capacitado para el MMA.",
            "monitor":"Los síntomas leves por exposición breve al vapor de MMA generalmente se resuelven con aire fresco y descanso.",
            "ok":     "Está seguro/a en el refugio. Los equipos de emergencia trabajan sin descanso.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Barlow',sans-serif;}
.stApp{background:#f0f4f8;}
.emergency-banner{
  background:linear-gradient(90deg,#7b0000,#c0392b);color:white;
  padding:14px 18px;border-radius:8px;font-weight:600;font-size:13px;
  margin-bottom:8px;border-left:5px solid #ff4444;line-height:1.6;
}
.hotline-bar{
  background:#003366;color:#7ec8e3;padding:10px 16px;border-radius:6px;
  font-size:12px;margin-bottom:16px;font-family:monospace;
}
.section-title{
  font-family:'Barlow Condensed',sans-serif;font-size:19px;font-weight:700;
  color:#003366;border-bottom:2px solid #003366;padding-bottom:4px;
  margin-top:22px;margin-bottom:10px;
}
.skin-section-title{
  font-family:'Barlow Condensed',sans-serif;font-size:19px;font-weight:700;
  color:#6b2d00;border-bottom:2px solid #cc7722;padding-bottom:4px;
  margin-top:22px;margin-bottom:10px;
}
.result-box{padding:20px;border-radius:10px;margin-top:16px;}
.result-911    {background:#fff0f0;border:3px solid #cc0000;}
.result-clinic {background:#fff8e6;border:3px solid #cc7700;}
.result-monitor{background:#f0fff4;border:3px solid #00aa44;}
.result-ok     {background:#f0f8ff;border:3px solid #0066cc;}
.result-title  {font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:800;margin-bottom:8px;}
.skin-alert{
  background:#fff3e0;border:2px solid #e65100;border-radius:8px;
  padding:12px 14px;font-size:13px;color:#4a1a00;margin-top:12px;line-height:1.6;
}
.disclaimer-box{
  background:#fffff0;border:1px solid #cccc00;border-radius:6px;
  padding:12px;font-size:12px;color:#666;margin-top:14px;line-height:1.6;
}
.mma-expander{background:#e8f4fd;border-left:4px solid #0066cc;padding:12px 16px;border-radius:4px;}
.powered{font-size:10px;color:#aaa;text-align:center;margin-top:24px;font-family:monospace;}
.share-box{background:#f8f8f8;border:1px dashed #999;border-radius:8px;padding:14px;font-size:13px;margin-top:8px;}
.free-badge{background:#003366;color:#fff;font-size:10px;font-weight:700;padding:3px 10px;border-radius:10px;letter-spacing:1px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
selected_lang = st.selectbox(
    "Language / Ngôn ngữ / Idioma",
    options=["English", "Tiếng Việt", "Español"],
    label_visibility="collapsed",
)
L = T[selected_lang]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown(f"# {L['title']}")
with col_badge:
    st.markdown('<br><span class="free-badge">100% FREE</span>', unsafe_allow_html=True)

st.caption(L["subtitle"])
st.markdown(f'<div class="emergency-banner">{L["banner"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hotline-bar">{L["hotlines"]}</div>', unsafe_allow_html=True)

with st.expander(L["what_is_mma"], expanded=False):
    st.markdown(L["mma_info"])

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# INTAKE FORM
# ─────────────────────────────────────────────────────────────────────────────

# Section 1 — Who
st.markdown(f'<div class="section-title">{L["section_who"]}</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age_group = st.selectbox(L["age_label"], L["age_opts"])
with col2:
    pregnant = st.selectbox(L["preg_label"], L["preg_opts"])
conditions = st.multiselect(L["cond_label"], L["cond_opts"])

# Section 2 — Exposure
st.markdown(f'<div class="section-title">{L["section_expo"]}</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    in_zone  = st.selectbox(L["expo_label"],      L["expo_opts"])
with col4:
    duration = st.selectbox(L["duration_label"],  L["duration_opts"])
skin_contact = st.selectbox(L["skin_expo_label"], L["skin_expo_opts"])

# Section 3 — Respiratory & Systemic
st.markdown(f'<div class="section-title">{L["section_symptoms"]}</div>', unsafe_allow_html=True)
symptoms = st.multiselect(L["sym_label"], L["sym_opts"])
onset    = st.selectbox(L["onset_label"], L["onset_opts"])

# Section 4 — Skin
st.markdown(f'<div class="skin-section-title">{L["section_skin"]}</div>', unsafe_allow_html=True)
skin_symptoms = st.multiselect(L["skin_sym_label"], L["skin_sym_opts"])

st.markdown("---")
st.info(
    "If anything feels wrong, trust your body and go to the medical station "
    "regardless of this result." if selected_lang == "English"
    else "Nếu cảm thấy có gì không ổn, hãy tin vào cơ thể và đến trạm y tế ngay." if selected_lang == "Tiếng Việt"
    else "Si algo se siente mal, confíe en su cuerpo y vaya a la estación médica."
)

# ─────────────────────────────────────────────────────────────────────────────
# TRIAGE ENGINE — rule-based, no API needed
# Evidence: EPA Tox Review MMA (2016), NIOSH, NCBI/IARC Vol.60
# ─────────────────────────────────────────────────────────────────────────────
def run_triage(age_group, pregnant, conditions, in_zone, duration,
               skin_contact, symptoms, skin_symptoms, onset, lang):

    # ── Map inputs to logic flags ─────────────────────────────────────────────
    age_map = {
        # EN
        "Child (0–12)": "child", "Teen (13–17)": "teen",
        "Adult (18–64)": "adult", "Senior (65+)": "senior",
        # VI
        "Trẻ em (0–12)": "child", "Thiếu niên (13–17)": "teen",
        "Người lớn (18–64)": "adult", "Người cao tuổi (65+)": "senior",
        # ES
        "Niño (0–12)": "child", "Adolescente (13–17)": "teen",
        "Adulto (18–64)": "adult", "Mayor (65+)": "senior",
    }
    age = age_map.get(age_group, "adult")

    preg = pregnant in ("Yes", "Có", "Sí", "Unsure", "Không chắc", "No estoy segura")
    preg_confirmed = pregnant in ("Yes", "Có", "Sí")

    high_risk_conds = {
        "Asthma", "Hen suyễn", "Asma",
        "COPD / Emphysema", "COPD / Khí thũng", "EPOC / Enfisema",
        "Heart disease / Arrhythmia", "Bệnh tim / Rối loạn nhịp", "Enfermedad cardíaca / Arritmia",
        "Skin allergy / Eczema history", "Dị ứng da / Chàm", "Alergia de piel / Eccema",
    }
    has_high_risk_cond = any(c in high_risk_conds for c in conditions)
    high_risk = age in ("child", "senior") or preg or has_high_risk_cond

    # Symptom classification
    severe_keywords = [
        "Shortness of breath", "Chest tightness", "Vomiting",
        "Khó thở", "Tức ngực", "Nôn mửa",
        "Dificultad para respirar", "Opresión", "Vómitos",
    ]
    neuro_keywords = [
        "Heaviness or weakness", "Lethargy",
        "Nặng nề hoặc yếu", "Mệt mỏi bất thường",
        "Pesadez o debilidad", "Letargo",
        "Palpitations", "Tim đập nhanh", "Palpitaciones",
    ]
    mild_keywords = [
        "Eye burning", "Runny nose", "Sore", "Coughing", "Wheezing",
        "Headache", "Dizziness", "Nausea",
        "Mắt bỏng", "Chảy nước mũi", "Đau họng", "Ho", "Khò khè",
        "Đau đầu", "Chóng mặt", "Buồn nôn",
        "Ardor", "Secreción", "Dolor de garganta", "Tos", "Sibilancias",
        "Dolor de cabeza", "Mareos", "Náuseas",
    ]
    severe_skin = [
        "Blistering", "spreading", "Phồng rộp", "lan ra", "ampollas", "extiende"
    ]
    mild_skin = [
        "redness", "Burning sensation", "Itching", "Numbness",
        "Đỏ da", "bỏng rát", "Ngứa", "Tê",
        "Enrojecimiento", "ardor", "Picazón", "Entumecimiento",
    ]

    has_severe  = any(any(k in s for k in severe_keywords) for s in symptoms)
    has_neuro   = any(any(k in s for k in neuro_keywords)  for s in symptoms)
    has_mild    = any(any(k in s for k in mild_keywords)   for s in symptoms)
    has_skin_sev = any(any(k in s for k in severe_skin)    for s in skin_symptoms)
    has_skin_mild = any(any(k in s for k in mild_skin)     for s in skin_symptoms)
    skin_exposed = skin_contact not in ("No", "Không", "No")

    # Delayed onset flag — 6-24h after exposure increases concern
    delayed = onset in (
        "6–24 hours ago", "More than 24 hours ago",
        "6–24 giờ trước", "Hơn 24 giờ trước",
        "Hace 6–24 horas", "Hace más de 24 horas",
    )

    # ── Decision tree ─────────────────────────────────────────────────────────
    if has_severe and high_risk:               return "911"
    if has_severe:                             return "clinic"
    if preg_confirmed:                         return "clinic"
    if has_neuro:                              return "clinic"
    if has_skin_sev:                           return "clinic"
    if high_risk and (has_mild or has_skin_mild): return "clinic"
    if delayed and (has_skin_mild or skin_exposed): return "clinic"
    if has_mild and in_zone in ("Yes — I was inside the zone", "Có — Tôi ở trong vùng", "Sí — estaba dentro de la zona"):
        return "monitor"
    if has_skin_mild or skin_exposed:          return "monitor"
    if has_mild:                               return "monitor"
    return "ok"

def render_result(level, L):
    colors = {
        "911":     ("#cc0000", "result-box result-911"),
        "clinic":  ("#cc7700", "result-box result-clinic"),
        "monitor": ("#007733", "result-box result-monitor"),
        "ok":      ("#0055bb", "result-box result-ok"),
    }
    color, css = colors[level]

    if level == "911":
        st.error("🚨 CALL 911 IMMEDIATELY — Do not wait.")

    st.markdown(
        f'<div class="{css}">'
        f'<div class="result-title" style="color:{color};">{L["levels"][level]}</div>'
        f'<p style="font-size:15px;font-weight:600;margin:0;">{L["headlines"][level]}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**What to do:**" if selected_lang == "English"
                    else "**Phải làm gì:**" if selected_lang == "Tiếng Việt"
                    else "**Qué hacer:**")
        for action in L["todo"][level]:
            st.markdown(f"▶ {action}")
    with col_b:
        st.markdown("**Watch for:**" if selected_lang == "English"
                    else "**Theo dõi dấu hiệu:**" if selected_lang == "Tiếng Việt"
                    else "**Señales de alerta:**")
        for sign in L["watch_for"][level]:
            st.markdown(f"🔴 {sign}")

    skin_note = L["skin_notes"].get(level, "")
    if skin_note:
        st.markdown(
            f'<div class="skin-alert">🩺 {skin_note}</div>',
            unsafe_allow_html=True,
        )

    st.info(L["reassurance"][level])
    st.markdown(f'<div class="hotline-bar">{L["hotlines"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="disclaimer-box">{L["disclaimer"]}</div>', unsafe_allow_html=True)

    # Anonymous session log — no PII
    if "session_log" not in st.session_state:
        st.session_state["session_log"] = []
    st.session_state["session_log"].append({
        "timestamp":     datetime.now().isoformat(),
        "language":      selected_lang,
        "age_group":     age_group,
        "pregnant":      pregnant,
        "conditions":    conditions,
        "in_zone":       in_zone,
        "duration":      duration,
        "skin_contact":  skin_contact,
        "symptoms":      symptoms,
        "skin_symptoms": skin_symptoms,
        "onset":         onset,
        "triage_level":  level,
    })

# ─────────────────────────────────────────────────────────────────────────────
# SUBMIT
# ─────────────────────────────────────────────────────────────────────────────
if st.button(L["submit_btn"], type="primary", use_container_width=True):
    st.markdown(f'<div class="section-title">{L["result_header"]}</div>', unsafe_allow_html=True)
    level = run_triage(
        age_group, pregnant, conditions, in_zone, duration,
        skin_contact, symptoms, skin_symptoms, onset, selected_lang
    )
    render_result(level, L)

# ─────────────────────────────────────────────────────────────────────────────
# SHARE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"**{L['share_header']}**")
st.markdown(L["share_text"])
st.markdown(
    '<div class="share-box">🔗 <b>https://mma-triage.streamlit.app</b><br>'
    '<span style="font-size:11px;color:#666;">'
    '(live after deploying to Streamlit Community Cloud — free)</span></div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="powered">{L["powered_by"]}</div>', unsafe_allow_html=True)
