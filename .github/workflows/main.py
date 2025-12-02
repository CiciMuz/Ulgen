import flet as ft

def main(page:ft.Page):
    page.title = "Gelir Gider"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            secondary_container=ft.Colors.AMBER,
            on_secondary_container=ft.Colors.BLACK,
            on_surface_variant=ft.Colors.WHITE,
            surface=ft.Colors.GREY_900,
        )
    )

    guncelpara=page.client_storage.get("guncelpara") or "0"

    # ------------------------------------------------------------------------------------------------------------------------
    def guncelpara_degistir(veri):
        nonlocal guncelpara
        tur=veri["Tür"]
        para=veri["Miktar"]
        temp = int(guncelpara) + int(para)
        guncelpara = str(temp)

        page.client_storage.set("guncelpara",guncelpara)

        log_olustur(veri)

        Guncel_Para_Field.value = f"Güncel Para= {guncelpara}"
        page.update()

    # ------------------------------------------------------------------------------------------------------------------------

    def duzenli_gelir_ekle(veri):

        mevcut_liste = page.client_storage.get("gelirler_listesi")
        if mevcut_liste is None:
            mevcut_liste = []
        tur=veri["Tür"]
        ad=veri["Ad"]
        miktar=veri["Miktar"]

        yeni_veri = {"Tür": tur,"Ad": ad, "Miktar": miktar}


        mevcut_liste.append(yeni_veri)


        page.client_storage.set("gelirler_listesi", mevcut_liste)

        print("Kayıt başarılı!")

    def duzenli_gelir_ekleme_ekrani(e=None):
        page.clean()

        ad_field = ft.TextField(label="Gelir Adı",border_color=ft.Colors.AMBER)
        miktar_field = ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)


        def onayla_tiklandi(e):

            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Gelir", "Ad": gelen_ad, "Miktar": gelen_miktar}

            duzenli_gelir_ekle(yeni_veri)


            duzenli_gelirler_ekrani()

        onayla = ft.ElevatedButton(text="Onayla", color=ft.Colors.AMBER,on_click=onayla_tiklandi,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))

        page.add(
            ust_bar,
            ft.Text("Yeni Gelir Ekle", size=20,color=ft.Colors.AMBER),
            ad_field,
            miktar_field,
            onayla,
            alt_bar
        )
        page.update()

    def duzenli_gelir_kaldir_yeni(silinecek_veri):
        yeni_liste = []
        silindi_mi = False

        yeni_liste = page.client_storage.get("gelirler_listesi") or []

        if silinecek_veri in yeni_liste:
            yeni_liste.remove(silinecek_veri)

        page.client_storage.set("gelirler_listesi", yeni_liste)

        duzenli_gelirler_ekrani()

    def duzenli_gelir_kaldirma_ekrani(e=None):
        page.clean()
        yeni_liste=page.client_storage.get("gelirler_listesi") or []

        gelir_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, height=400)
        gelir_column.controls.append(ft.Text("SİLMEK İSTEDİĞİNİZ GELİRE TIKLAYIN", color="red", weight="bold"))



        for veri in yeni_liste:

            ad=veri["Ad"]
            miktar=veri["Miktar"]

            temp_buton = ft.ElevatedButton(
                text=f"Gelir adı: {ad}\nMiktarı: {miktar}",
                height=75,
                width=225,
                color="red",
                bgcolor="black",
                style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)),
            on_click=lambda e, v=veri: duzenli_gelir_kaldir_yeni(v)
            )
            gelir_column.controls.append(temp_buton)


        geri_don = ft.ElevatedButton("Geri Dön",color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)), on_click=lambda _: duzenli_gelirler_ekrani())

        page.add(ust_bar, ana_row, gelir_column, geri_don, alt_bar)
        page.update()

    def duzenli_gelirler_ekrani():
        page.clean()

        eslesmeler=page.client_storage.get("gelirler_listesi") or []

        gelir_column=ft.Column(alignment=ft.MainAxisAlignment.CENTER,height=400,scroll=ft.ScrollMode.AUTO)
        ekle_butonu=ft.ElevatedButton(text="Gelir Ekle",width=150,on_click=duzenli_gelir_ekleme_ekrani,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        kaldir_butonu = ft.ElevatedButton(text="Gelir Kaldır",width=150, on_click=duzenli_gelir_kaldirma_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        butonlar_rowu=ft.Row(controls=[ekle_butonu,kaldir_butonu],alignment=ft.MainAxisAlignment.CENTER)
        for veri in eslesmeler:
            ad = veri["Ad"]
            miktar = veri["Miktar"]
            temp_buton=ft.ElevatedButton(text=f"Gelir Adı: {ad}\nMiktar: {miktar}",height=75,width=225,color=ft.Colors.AMBER,on_click=lambda e, v=veri: guncelpara_degistir(v),style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
            gelir_column.controls.append(temp_buton)

        ayirici = ft.Row(
            controls=[
                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),


                ft.Text("  Kayıtlı İşlemler  ", color=ft.Colors.GREY_500, italic=True, weight="bold"),


                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(ust_bar,ana_row,butonlar_rowu,ft.Text(value="\n"),ayirici,gelir_column,alt_bar)
        page.update()

# ------------------------------------------------------------------------------------------------------------------------

    def log_temizleme(e=None):
        temp=[]
        page.client_storage.set("tum_log", temp)
        ana_ekrani()

    def log_temizle_ekrani(e=None):
        page.clean()
        yazi = ft.Text(value="Geçmişi temizlemek istediğinize emin misiniz?")
        evet = ft.ElevatedButton(text="Evet",color=ft.Colors.AMBER,on_click=log_temizleme,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        hayir = ft.ElevatedButton(text="Hayır",on_click=ana_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        page.add(ust_bar,yazi,evet,hayir,alt_bar)

    def yeni_veri_ekrani_gelir_gider_ekleme(ad,miktar):
        if int(miktar)<0:
            yeni_veri = {"Tür": "Gider", "Ad": ad, "Miktar": miktar}
        else:
            yeni_veri = {"Tür": "Gelir", "Ad": ad, "Miktar": miktar}
        guncelpara_degistir(yeni_veri)

    def yeni_veri_ekrani(e=None):
        page.clean()
        ad_bari=ft.TextField(label="Ad",border_color=ft.Colors.AMBER)
        girdi_bari=ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)
        log_temizleme_butonu=ft.ElevatedButton(text="Geçmişi Temizle...",on_click=log_temizle_ekrani,color=ft.Colors.LIGHT_BLUE_ACCENT_400,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.LIGHT_BLUE_ACCENT_700)))

        def islem_yap(ad,miktar):
            yeni_veri_ekrani_gelir_gider_ekleme(ad,miktar)
            ana_ekrani()


        gelir_butonu=ft.ElevatedButton(text="      Gelir      ",on_click=lambda e:islem_yap(ad_bari.value,girdi_bari.value),color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        gider_butonu = ft.ElevatedButton(text="      Gider      ",on_click=lambda e:islem_yap(ad_bari.value,str(-1*int(girdi_bari.value))),color=ft.Colors.RED,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        page.add(
            ad_bari,
            girdi_bari,
            alt_bar,
            ust_bar,
            gelir_butonu,
            gider_butonu,
            log_temizleme_butonu,
        )
        page.update()

    def guncelpara_sifirla_ekran(e=None):
        page.clean()
        text=ft.Text(value="Sıfırlamak istediğinize emin misiniz?")
        evet = ft.ElevatedButton(text="Evet", on_click=guncelpara_sifirla,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        hayir = ft.ElevatedButton(text="Hayır", on_click=ana_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        page.add(
            text,
            evet,
            hayir,
            alt_bar,
            ust_bar
        )
        page.update()


    def guncelpara_sifirla(e=None):
        nonlocal guncelpara
        deger=str(-1*int(guncelpara))
        yeni_veri = {"Tür": "Gider", "Ad": "Sıfırlama İşlemi", "Miktar": deger}
        guncelpara_degistir(yeni_veri)
        ana_ekrani()



    def ana_ekrani():
        page.clean()
        eslesmeler=page.client_storage.get("tum_log") or []


        yeni_veri_ekrani_butonu=ft.ElevatedButton(text="Yeni veri ekle",on_click=yeni_veri_ekrani,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        log_column=ft.Column(alignment=ft.MainAxisAlignment.CENTER,scroll=ft.ScrollMode.AUTO,height=350)

        para_sifirla=ft.ElevatedButton(text="Bakiye sıfırla...",on_click=guncelpara_sifirla_ekran,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        for veri in eslesmeler:
            tur=veri["Tür"]
            ad=veri["Ad"]
            miktar=veri["Miktar"]
            if tur=="Gelir":
                temp=ft.TextField(multiline=True,value=f"Açıklama: {ad}\nMiktar: {miktar}",border_color=ft.Colors.AMBER,read_only=True)
                log_column.controls.append(temp)
            elif tur=="Gider":
                temp = ft.TextField(multiline=True,value=f"Açıklama: {ad}\nMiktar: {miktar}", border_color="red",read_only=True)
                log_column.controls.append(temp)

        log_column.controls = log_column.controls[::-1]
        butonlar_row=ft.Row(controls=[yeni_veri_ekrani_butonu,para_sifirla],alignment=ft.MainAxisAlignment.CENTER)

        ayirici = ft.Row(
            controls=[
                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),


                ft.Text("  Geçmiş İşlemler  ", color=ft.Colors.GREY_500, italic=True,weight="bold"),


                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(
            ana_row,
            butonlar_row,
            ft.Text(value="\n"),
            ayirici,
            ft.Text(value="\n"),
            log_column,
            ust_bar,
            alt_bar,
        )
        page.update()

# ------------------------------------------------------------------------------------------------------------------------

    def log_olustur(veri):
        log=page.client_storage.get("tum_log") or []
        log.append(veri)
        page.client_storage.set("tum_log", log)

# ------------------------------------------------------------------------------------------------------------------------

    def duzenli_gider_ekle(veri):


        mevcut_liste = page.client_storage.get("giderler_listesi")
        if mevcut_liste is None:
            mevcut_liste = []
        tur=veri["Tür"]
        ad=veri["Ad"]
        miktar=veri["Miktar"]

        yeni_veri = {"Tür": tur,"Ad": ad, "Miktar": str(-1*int(miktar))}

        mevcut_liste.append(yeni_veri)
        page.client_storage.set("giderler_listesi", mevcut_liste)

        print("Kayıt başarılı!")

    def duzenli_gider_ekleme_ekrani(e=None):
        page.clean()

        ad_field = ft.TextField(label="Gider Adı",border_color=ft.Colors.AMBER)
        miktar_field = ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)

        def onayla_tiklandi(e):
            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Gider", "Ad": gelen_ad, "Miktar": gelen_miktar}
            duzenli_gider_ekle(yeni_veri)


            duzenli_giderler_ekrani()

        onayla = ft.ElevatedButton(text="Onayla", on_click=onayla_tiklandi,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))

        page.add(
            ft.Text("Yeni Gider Ekle", size=20,color=ft.Colors.AMBER),
            ad_field,
            miktar_field,
            onayla,
            alt_bar
        )
        page.update()

    def duzenli_gider_kaldir_yeni(silinecek_veri):
        yeni_liste = []
        silindi_mi = False

        yeni_liste = page.client_storage.get("giderler_listesi") or []

        if silinecek_veri in yeni_liste:
            yeni_liste.remove(silinecek_veri)

        page.client_storage.set("giderler_listesi", yeni_liste)

        duzenli_giderler_ekrani()

    def duzenli_gider_kaldirma_ekrani(e=None):
        page.clean()
        yeni_liste=page.client_storage.get("giderler_listesi") or []

        gider_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, height=400)
        gider_column.controls.append(ft.Text("SİLMEK İSTEDİĞİNİZ GİDERE TIKLAYIN", color="red", weight="bold"))



        for veri in yeni_liste:

            ad=veri["Ad"]
            miktar=veri["Miktar"]

            temp_buton = ft.ElevatedButton(
                text=f"Gider adı: {ad}\nMiktarı: {miktar}",
                height=75,
                width=225,
                color="red",
                bgcolor="black",
                style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)),
                on_click=lambda e, v=veri: duzenli_gider_kaldir_yeni(v)
            )
            gider_column.controls.append(temp_buton)


        geri_don = ft.ElevatedButton("Geri Dön", on_click=lambda _: duzenli_giderler_ekrani(),color="red",style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        page.add(ust_bar, ana_row, gider_column, geri_don, alt_bar)
        page.update()

    def duzenli_giderler_ekrani():
        page.clean()

        eslesmeler=page.client_storage.get("giderler_listesi") or []

        gider_column=ft.Column(alignment=ft.MainAxisAlignment.CENTER,height=400,scroll=ft.ScrollMode.AUTO)
        ekle_butonu=ft.ElevatedButton(text="Gider Ekle",width=150,on_click=duzenli_gider_ekleme_ekrani,color=ft.Colors.AMBER,style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        kaldir_butonu = ft.ElevatedButton(text="Gider Kaldır",width=150, on_click=duzenli_gider_kaldirma_ekrani,color="red",style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        butonlar_rowu=ft.Row(controls=[ekle_butonu,kaldir_butonu],alignment=ft.MainAxisAlignment.CENTER)
        for veri in eslesmeler:
            ad = veri["Ad"]
            miktar = veri["Miktar"]
            temp_buton=ft.ElevatedButton(text=f"Gider Adı: {ad}\nMiktar: {miktar}",height=75,width=225,on_click=lambda e, v=veri: guncelpara_degistir(v),color="red",style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
            gider_column.controls.append(temp_buton)

        ayirici = ft.Row(
            controls=[
                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),


                ft.Text("  Kayıtlı İşlemler  ", color=ft.Colors.GREY_500, italic=True, weight="bold"),


                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER  # Çizgileri yazıyla hizalar
        )

        page.add(ust_bar,ana_row,butonlar_rowu,ft.Text(value="\n"),ayirici,gider_column,alt_bar)
        page.update()

# ------------------------------------------------------------------------------------------------------------------------

    def ekran_degistir(e):
        indis = e.control.selected_index

        page.clean()

        if indis == 0:
            duzenli_gelirler_ekrani()
        elif indis == 1:
            ana_ekrani()
        elif indis == 2:
            duzenli_giderler_ekrani()

    # ------------------------------------------------------------------------------------------------------------------------
    Guncel_Para_Field=ft.TextField(value=f"Güncel Para: {guncelpara}",read_only=True,text_size=20,width=300,height=60,color=ft.Colors.AMBER,border_color=ft.Colors.AMBER_700,border_width=4)
    ana_row=ft.Row(controls=[Guncel_Para_Field],alignment=ft.MainAxisAlignment.CENTER)

    ust_bar = ft.AppBar(
        title=ft.Image(src="ulgen.png", height=40),
        center_title=True,
        color="black",
        bgcolor=ft.Colors.AMBER,
        automatically_imply_leading=False,
    )

    alt_bar = ft.NavigationBar(
        indicator_color=ft.Colors.AMBER,

        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.ATTACH_MONEY, label="Düzenli Gelirler"),
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Ana Ekran"),
            ft.NavigationBarDestination(icon=ft.Icons.MONEY_OFF, label="Düzenli Giderler"),
        ],
        selected_index=1,
        on_change=ekran_degistir

    )
    ana_ekrani()



ft.app(target=main, assets_dir="assets")
