
# PROJECTS – LIST PAGE
# ==============================================

projects_data = [
    {
        "id": 1,
        "slug": "casa-blanca-garden",
        "title": "Casa Blanca Garden",
        "Project_type": "Villa garden",
        "Area": "500m2",
        "Year": "2024",
        "Design": "H2 & H+",
        "Generalcontractor": "H+",
        "Status": "Built",
        "description": "…",
        "featured": True,

        "featured_images": [
            "/static/projects/casa/1.jpg",
            "/static/projects/casa/2.jpg",
            "/static/projects/casa/3.jpg",
            "/static/projects/casa/4.jpg",
            "/static/projects/casa/5.jpg",
            "/static/projects/casa/6.jpg",
            "/static/projects/casa/7.jpg",
            "/static/projects/casa/8.jpg",
            "/static/projects/casa/9.jpg",
        ],

        "images": [f"/static/projects/casa/{i}.jpg" for i in range(1, 46)]
    },

    # -----------------------------------------------------
    {
        "id": 2,
        "slug": "cho-lach-house",
        "title": "Chợ Lách House",
        "Project_type": "villa garden",
        "Area": "300m2",
        "Year": "2025",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/cho_lach_garden/1.jpg",
            "/static/projects/cho_lach_garden/2.jpg",
            "/static/projects/cho_lach_garden/3.jpg",
            "/static/projects/cho_lach_garden/4.jpg",
            "/static/projects/cho_lach_garden/5.jpg",
            "/static/projects/cho_lach_garden/6.jpg",
            "/static/projects/cho_lach_garden/7.jpg",
            "/static/projects/cho_lach_garden/8.jpg",
            "/static/projects/cho_lach_garden/9.jpg",

         ],

        "images": [f"/static/projects/cho_lach_garden/{i}.jpg" for i in range(1, 18)]
    },
    

    # -----------------------------------------------------

    {
        "id": 3,
        "slug": "truong-cong-dinh-house",
        "title": "Trương Công Định House",
        "Project_type": "Townhouse",
        "Area": "200m2",
        "Year": "2025",
        "Design": "H2 & H+",
        "Generalcontractor": "H+",
        "Status": "Built",
        "description": "…",

        "featured_images": [
            "/static/projects/nha_tcd/1.jpg",
            "/static/projects/nha_tcd/2.jpg",
            "/static/projects/nha_tcd/3.jpg",
            "/static/projects/nha_tcd/4.jpg",
            "/static/projects/nha_tcd/5.jpg",
            "/static/projects/nha_tcd/6.jpg",
            "/static/projects/nha_tcd/7.jpg",
            "/static/projects/nha_tcd/8.jpg",
            "/static/projects/nha_tcd/9.jpg",
        ],

        "images": [f"/static/projects/nha_tcd/{i}.jpg" for i in range(1, 10)]
    },

    # -----------------------------------------------------
    {
        "id": 4,
        "slug": "dongho_kg",
        "title": "Đông Hồ Kiên Giang Resort",
        "Project_type": "resort",
        "Area": "15000m2",
        "Year": "2025",
        "Design": "H2 & H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/dongho_kg/1.jpg",
            "/static/projects/dongho_kg/2.jpg",
            "/static/projects/dongho_kg/3.jpg",
            "/static/projects/dongho_kg/4.jpg",
            "/static/projects/dongho_kg/5.jpg",
            "/static/projects/dongho_kg/6.jpg",
            "/static/projects/dongho_kg/7.jpg",
            "/static/projects/dongho_kg/8.jpg",
            "/static/projects/dongho_kg/9.jpg",
        ],

        "images": [f"/static/projects/dongho_kg/{i}.jpg" for i in range(1, 34)]
    },

    # -----------------------------------------------------
    {
        "id": 5,
        "slug": "happy-garden-retreat",
        "title": "Happy Garden Retreat",
        "Project_type": "resort",
        "Area": "3000m2",
        "Year": "2025",
        "Design": "H2 & H+",
        "Status": "Concept",
        "description": "…",
        "featured": True,

        "featured_images": [
            "/static/projects/happy garden retreat/1.jpg",
            "/static/projects/happy garden retreat/2.jpg",
            "/static/projects/happy garden retreat/3.jpg",
            "/static/projects/happy garden retreat/4.jpg",
            "/static/projects/happy garden retreat/5.jpg",
            "/static/projects/happy garden retreat/6.jpg",
            "/static/projects/happy garden retreat/7.jpg",
            "/static/projects/happy garden retreat/8.jpg",
            "/static/projects/happy garden retreat/9.jpg",
        ],

        "images": [f"/static/projects/happy garden retreat/{i}.jpg" for i in range(1, 20)]
    },

    # -----------------------------------------------------
    {
        "id": 6,
        "slug": "thanhoai_house",
        "title": "Thanh Oai House",
        "Project_type": "Townhouse",
        "Area": "200m2",
        "Year": "2025",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",


        "featured_images": [
            "/static/projects/thanhoai_house/1.jpg",
            "/static/projects/thanhoai_house/2.jpg",
            "/static/projects/thanhoai_house/3.jpg",
            "/static/projects/thanhoai_house/4.jpg",
            "/static/projects/thanhoai_house/5.jpg",
            "/static/projects/thanhoai_house/6.jpg",
            "/static/projects/thanhoai_house/7.jpg",
            "/static/projects/thanhoai_house/8.jpg",
            "/static/projects/thanhoai_house/9.jpg",
        ],

        "images": [f"/static/projects/thanhoai_house/{i}.jpg" for i in range(1, 13)]
    },
  # -----------------------------------------------------
    {
        "id": 7,
        "slug": "vt_sunset",
        "title": "Vũng Tàu Sunset",
        "Project_type": "Townhouse",
        "Area": "300m2",
        "Year": "2023",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",


        "featured_images": [
            "/static/projects/vt_sunset/1.jpg",
            "/static/projects/vt_sunset/2.jpg",
            "/static/projects/vt_sunset/3.jpg",
            "/static/projects/vt_sunset/4.jpg",
            "/static/projects/vt_sunset/5.jpg",
            "/static/projects/vt_sunset/6.jpg",
            "/static/projects/vt_sunset/7.jpg",
            "/static/projects/vt_sunset/8.jpg",
            "/static/projects/vt_sunset/9.jpg",
        ],

        "images": [f"/static/projects/vt_sunset/{i}.jpg" for i in range(1, 13)]
    },
  # -----------------------------------------------------
    {
        "id": 8,
        "slug": "moon-cafe",
        "title": "Moon Café",
        "Project_type": "Coffee shop",
        "Area": "150m2",
        "Year": "2023",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/moon_cafe/1.jpg",
            "/static/projects/moon_cafe/2.jpg",
            "/static/projects/moon_cafe/3.jpg",
            "/static/projects/moon_cafe/4.jpg",
            "/static/projects/moon_cafe/5.jpg",
            "/static/projects/moon_cafe/6.jpg",
            "/static/projects/moon_cafe/7.jpg",
            "/static/projects/moon_cafe/8.jpg",
            "/static/projects/moon_cafe/9.jpg",
        ],

        "images": [f"/static/projects/moon_cafe/{i}.jpg" for i in range(1, 10)]
    },

    # -----------------------------------------------------
    {
        "id": 9,
        "slug": "vif-office",
        "title": "Tập Đoàn VFI",
        "Project_type": "Office",
        "Area": "1000m2",
        "Year": "2023",
        "Design": "H+",
        "Generalcontractor": "H+",
        "Status": "Built",
        "description": "…",
        "featured": True,

        "featured_images": [
            "/static/projects/vfi/1.jpg",
            "/static/projects/vfi/2.jpg",
            "/static/projects/vfi/3.jpg",
            "/static/projects/vfi/4.jpg",
            "/static/projects/vfi/5.jpg",
            "/static/projects/vfi/6.jpg",
            "/static/projects/vfi/7.jpg",
            "/static/projects/vfi/8.jpg",
            "/static/projects/vfi/9.jpg",
        ],

        "images": [f"/static/projects/vfi/{i}.jpg" for i in range(1, 63)]
    },

    # -----------------------------------------------------
    {
        "id": 10,
        "slug": "tran-xuan-do-house",
        "title": "Trần Xuân Độ House",
        "Project_type": "Townhouse",
        "Area": "160m2",
        "Year": "2023",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/tran_xuan_do/1.jpg",
            "/static/projects/tran_xuan_do/2.jpg",
            "/static/projects/tran_xuan_do/3.jpg",
            "/static/projects/tran_xuan_do/4.jpg",
            "/static/projects/tran_xuan_do/5.jpg",
            "/static/projects/tran_xuan_do/6.jpg",
            "/static/projects/tran_xuan_do/7.jpg",
            "/static/projects/tran_xuan_do/8.jpg",
            "/static/projects/tran_xuan_do/9.jpg",
        ],

        "images": [f"/static/projects/tran_xuan_do/{i}.jpg" for i in range(1, 18)]
    },
# -----------------------------------------------------
    {
        "id": 11,
        "slug": "thao-dien-arpartment",
        "title": "Thảo Điền Apartment",
        "Project_type": "Apartment",
        "Area": "70m2",
        "Year": "2023",
        "Design": "H2 & H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/thao_dien_apartment/1.jpg",
            "/static/projects/thao_dien_apartment/2.jpg",
            "/static/projects/thao_dien_apartment/3.jpg",
            "/static/projects/thao_dien_apartment/4.jpg",
            "/static/projects/thao_dien_apartment/5.jpg",
            "/static/projects/thao_dien_apartment/6.jpg",
            "/static/projects/thao_dien_apartment/7.jpg",
            "/static/projects/thao_dien_apartment/8.jpg",
            "/static/projects/thao_dien_apartment/9.jpg",
        ],

        "images": [f"/static/projects/thao_dien_apartment/{i}.jpg" for i in range(1, 11)]
    },

# -----------------------------------------------------
    {
        "id": 12,
        "slug": "daian_arpartment",
        "title": "Đại An Apartment",
        "Project_type": "Apartment",
        "Area": "70m2",
        "Year": "2021",
        "Design": "H2",
        "Generalcontractor": "H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/daian_apartment/1.jpg",
            "/static/projects/daian_apartment/2.jpg",
            "/static/projects/daian_apartment/3.jpg",
            "/static/projects/daian_apartment/4.jpg",
            "/static/projects/daian_apartment/5.jpg",
            "/static/projects/daian_apartment/6.jpg",
            "/static/projects/daian_apartment/7.jpg",
            "/static/projects/daian_apartment/8.jpg",
            "/static/projects/daian_apartment/9.jpg",
        ],

        "images": [f"/static/projects/daian_apartment/{i}.jpg" for i in range(1, 17)]
    },
# -----------------------------------------------------
    {
        "id": 13,
        "slug": "levanhuan",
        "title": "Lê Văn Huân Apartment",
        "Project_type": "Apartment",
        "Area": "150m2",
        "Year": "2020",
        "Design": "H+",
        "Status": "Concept",
        "description": "…",

        "featured_images": [
            "/static/projects/levanhuan/1.jpg",
            "/static/projects/levanhuan/2.jpg",
            "/static/projects/levanhuan/3.jpg",
            "/static/projects/levanhuan/4.jpg",
            "/static/projects/levanhuan/5.jpg",
            "/static/projects/levanhuan/6.jpg",
            "/static/projects/levanhuan/7.jpg",
            "/static/projects/levanhuan/8.jpg",
            "/static/projects/levanhuan/9.jpg",
        ],

        "images": [f"/static/projects/levanhuan/{i}.jpg" for i in range(1, 28)]
    },


]


