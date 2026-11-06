import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Bedah Kasus 2 - Profil Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dataset_profil_mahasiswa.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset_profil_mahasiswa.csv: {e}")
    st.stop()

# 3. Sidebar Filter
st.sidebar.title("📌 Filter Profil")

jurusan_list = list(df['Jurusan'].unique())
jurusan_filter = st.sidebar.multiselect(
    "Pilih Jurusan:",
    options=jurusan_list,
    default=jurusan_list
)

semester_list = sorted(list(df['Semester'].unique()))
semester_filter = st.sidebar.multiselect(
    "Pilih Semester (Ordinal):",
    options=semester_list,
    default=semester_list
)

filtered_df = df[
    (df['Jurusan'].isin(jurusan_filter)) &
    (df['Semester'].isin(semester_filter))
]

# 4. Header & Ringkasan KPI
st.title("🎓 Bedah Kasus 2: Dataset Profil Mahasiswa")
st.caption("Visualisasi Data Nominal, Ordinal, dan Kontinu")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Mahasiswa", f"{len(filtered_df)} orang")
with col2:
    avg_ipk = filtered_df['IPK'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata IPK", f"{avg_ipk:.2f}")
with col3:
    avg_age = filtered_df['Usia'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Usia", f"{avg_age:.1f} tahun")
with col4:
    max_ipk = filtered_df['IPK'].max() if len(filtered_df) > 0 else 0
    st.metric("IPK Tertinggi", f"{max_ipk:.2f}")

st.markdown("---")

# 5. Tab Visualisasi Bedah Kasus 2
tab1, tab2, tab3, tab4 = st.tabs([
    "🏷️ Nominal (Jurusan)", 
    "📊 Ordinal (Semester)", 
    "🔢 Kontinu (IPK & Usia)", 
    "📋 Data Mentah"
])

# Tab 1: Kategorik Nominal (Jurusan)
with tab1:
    st.subheader("1. Distribusi Mahasiswa per Jurusan (Kategorik Nominal)")
    st.write("*Tipe Data: Nominal | Visualisasi: Bar Chart / Pie Chart*")
    
    col_a, col_b = st.columns(2)
    with col_a:
        jur_count = filtered_df['Jurusan'].value_counts().reset_index()
        jur_count.columns = ['Jurusan', 'Jumlah']
        fig_bar_jur = px.bar(
            jur_count, x='Jurusan', y='Jumlah',
            title='Jumlah Mahasiswa per Jurusan',
            color='Jurusan',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_bar_jur, use_container_width=True)
        
    with col_b:
        fig_pie_jur = px.pie(
            jur_count, values='Jumlah', names='Jurusan',
            title='Proporsi Mahasiswa per Jurusan',
            hole=0.3
        )
        st.plotly_chart(fig_pie_jur, use_container_width=True)

# Tab 2: Kategorik Ordinal (Semester)
with tab2:
    st.subheader("2. Sebaran Mahasiswa per Semester (Kategorik Ordinal)")
    st.write("*Tipe Data: Ordinal (Ada tingkatan urutan 1 -> 2 -> 3 dst.) | Visualisasi: Bar Chart Berurutan*")
    
    sem_count = filtered_df.groupby('Semester').size().reset_index(name='Jumlah Mahasiswa')
    sem_count = sem_count.sort_values('Semester')
    sem_count['Semester_Label'] = 'Semester ' + sem_count['Semester'].astype(str)
    
    fig_sem = px.bar(
        sem_count, x='Semester_Label', y='Jumlah Mahasiswa',
        title='Distribusi Mahasiswa Berdasarkan Tingkat Semester',
        color='Semester_Label',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_sem.update_layout(xaxis_title="Tingkat Semester", yaxis_title="Jumlah Mahasiswa")
    st.plotly_chart(fig_sem, use_container_width=True)

# Tab 3: Numerik Kontinu (IPK & Usia)
with tab3:
    st.subheader("3. Distribusi dan Sebaran IPK & Usia (Numerik Kontinu)")
    st.write("*Tipe Data: Kontinu (Rentang/Desimal) | Visualisasi: Histogram & Box Plot*")
    
    col_c, col_d = st.columns(2)
    with col_c:
        fig_ipk_hist = px.histogram(
            filtered_df, x='IPK', color='Jurusan', nbins=10,
            title='Distribusi Frekuensi IPK (Histogram)',
            marginal='box',
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        st.plotly_chart(fig_ipk_hist, use_container_width=True)
        
    with col_d:
        fig_box_ipk = px.box(
            filtered_df, x='Jurusan', y='IPK', color='Jurusan',
            points="all",
            title='Sebaran & Outlier IPK per Jurusan (Box Plot)'
        )
        st.plotly_chart(fig_box_ipk, use_container_width=True)

# Tab 4: Data Mentah
with tab4:
    st.subheader("📋 Explorer Data Mentah Profil Mahasiswa")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data (CSV)",
        data=csv,
        file_name='data_profil_mahasiswa.csv',
        mime='text/csv',
    )