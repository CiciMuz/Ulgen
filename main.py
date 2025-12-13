import flet as ft
from datetime import datetime

from flet.core.border_radius import horizontal


def main(page:ft.Page):
    page.title = "Gelir Gider"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"

    def tam_zaman_getir():
        an = datetime.now()
        return an.strftime("%d.%m.%Y %H:%M")


    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            secondary_container=ft.Colors.AMBER,
            on_secondary_container=ft.Colors.BLACK,
            on_surface_variant=ft.Colors.WHITE,
            surface=ft.Colors.GREY_900,
        ),
        navigation_bar_theme=ft.NavigationBarTheme(
            label_text_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.W_500
            )
        )
    )

#-------------------------------------------------------------------------------------------------------------
    def borc_ekrani():
        return

    def borc_ekle(veri)->bool:

        kontrol=veri["Miktar"]

        try:
            int(kontrol)
        except:
            print("Terminal Girdisi: Hata")
            return False



        mevcut_liste = page.client_storage.get("borclar_listesi")

        if mevcut_liste is None or not isinstance(mevcut_liste, list):
            mevcut_liste = []

        tur=veri["Tür"]
        ad=veri["Ad"]
        miktar=veri["Miktar"]
        tarih=veri["Tarih"]

        yeni_veri = {"Tür": tur,"Ad": ad, "Miktar": miktar, "Tarih": tarih}


        mevcut_liste.append(yeni_veri)


        page.client_storage.set("borclar_listesi", mevcut_liste)

        print("Kayıt başarılı!")
        return True

    def borc_ekleme_ekrani(e=None):
        page.clean()
        page.scroll = "auto"

        ad_field = ft.TextField(label="Borç:",border_color=ft.Colors.AMBER)
        miktar_field = ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)

        def onayla_tiklandi_alinan(e):

            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Borc", "Ad": gelen_ad, "Miktar": gelen_miktar, "Tarih": tam_zaman_getir()}

            sonuc=borc_ekle(yeni_veri)

            guncelpara_degistir(yeni_veri)

            if sonuc== True:
                borc_ekrani()
            else:
                print("")

        def onayla_tiklandi_verilen(e):

            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Borc", "Ad": gelen_ad, "Miktar": str(-1*(int(gelen_miktar))), "Tarih": tam_zaman_getir()}

            sonuc=borc_ekle(yeni_veri)

            guncelpara_degistir(yeni_veri)

            if sonuc== True:
                borc_ekrani()
            else:
                print("")

        alinan=ft.ElevatedButton(text="Alınan", color=ft.Colors.AMBER,on_click=onayla_tiklandi_alinan,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        verilen=ft.ElevatedButton(text="Verilen", color=ft.Colors.RED,on_click=onayla_tiklandi_verilen,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))



        page.add(
            ft.Text("Yeni Borç Ekle", size=20,color=ft.Colors.AMBER),
            ad_field,
            miktar_field,
            verilen,
            alinan,
            konteyner,
        )
        page.update()

    def borc_kaldir_yeni(silinecek_veri):
        yeni_liste = []
        silindi_mi = False

        yeni_liste = page.client_storage.get("borclar_listesi") or []

        if silinecek_veri in yeni_liste:
            yeni_liste.remove(silinecek_veri)

        page.client_storage.set("borclar_listesi", yeni_liste)

        borc_ekrani()

    def borc_kaldirma_ekrani(e=None):
        page.clean()
        page.scroll = "auto"
        yeni_liste=page.client_storage.get("borclar_listesi") or []

        alinacak_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        verilecek_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

        text=ft.Text("SİLMEK İSTEDİĞİNİZ BORCA TIKLAYIN", color="red", weight="bold")


        def hem_sil_hem_guncelle(veri,e=None):
            tur = veri["Tür"]
            ad = veri["Ad"]
            miktar = veri["Miktar"]
            tarih = veri["Tarih"]

            yeni_veri = {"Tür": tur, "Ad": ad, "Miktar": str(-1*int(miktar)), "Tarih": tarih}
            borc_kaldir_yeni(veri)
            guncelpara_degistir(yeni_veri)


        for veri in yeni_liste:

            ad = veri["Ad"]
            miktar = veri["Miktar"]

            if int(miktar) < 0:
                temp_buton = ft.ElevatedButton(
                    text=f"Açıklama: {ad}\nAlınacak: {str(-1 * int(miktar))}",
                    height=75,
                    width=225,
                    color=ft.Colors.AMBER,
                    bgcolor="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),side=ft.BorderSide(width=2, color=ft.Colors.AMBER)),
                    on_click=lambda e, v=veri: hem_sil_hem_guncelle(v)
                )
                verilecek_column.controls.append(temp_buton)
            else:
                temp_buton = ft.ElevatedButton(
                    text=f"Açıklama: {ad}\nVerilecek: {str(-1 * int(miktar))}",
                    height=75,
                    width=225,
                    color="red",
                    bgcolor="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),side=ft.BorderSide(width=2, color=ft.Colors.RED)),
                    on_click=lambda e, v=veri: hem_sil_hem_guncelle(v),

                )
                alinacak_column.controls.append(temp_buton)

        ayirici = ft.Row(
            controls=[
                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),

                ft.Text("  Alınacaklar     -     Verilecekler  ", color=ft.Colors.GREY_500, italic=True, weight="bold"),

                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        orta_ayirici = ft.Container(width=2, height=500, bgcolor=ft.Colors.GREY_700)

        sol_panel = ft.Container(content=verilecek_column, expand=1, alignment=ft.alignment.top_center)
        sag_panel = ft.Container(content=alinacak_column, expand=1, alignment=ft.alignment.top_center)


        butonlar_row = ft.Row(
            controls=[sol_panel, orta_ayirici, sag_panel],
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0
        )


        page.add(text, ayirici, butonlar_row, konteyner)
        page.update()

    def borc_ekrani():
        page.clean()

        page.scroll="auto"

        eslesmeler=page.client_storage.get("borclar_listesi") or []

        ekle_butonu=ft.ElevatedButton(text="Borç Ekle",width=150,on_click=borc_ekleme_ekrani,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        kaldir_butonu = ft.ElevatedButton(text="Borç Kaldır",width=150, on_click=borc_kaldirma_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        eklekaldir=ft.Row(controls=[ekle_butonu,kaldir_butonu],alignment=ft.MainAxisAlignment.CENTER)
        yeni_liste = page.client_storage.get("borclar_listesi") or []

        alinacak_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        verilecek_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

        def hem_sil_hem_guncelle(veri,e=None):
            tur = veri["Tür"]
            ad = veri["Ad"]
            miktar = veri["Miktar"]
            tarih = veri["Tarih"]

            yeni_veri = {"Tür": tur, "Ad": ad, "Miktar": str(-1*int(miktar)), "Tarih": tarih}

            borc_kaldir_yeni(veri)
            guncelpara_degistir(yeni_veri)

        for veri in yeni_liste:

            ad = veri["Ad"]
            miktar = veri["Miktar"]

            if int(miktar) < 0:
                temp_buton = ft.ElevatedButton(
                    text=f"Açıklama: {ad}\nAlınacak: {str(-1*int(miktar))}",
                    height=75,
                    width=225,
                    color=ft.Colors.AMBER,
                    bgcolor="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),side=ft.BorderSide(width=2, color=ft.Colors.AMBER)),
                    on_click=lambda e, v=veri: hem_sil_hem_guncelle(v)
                )
                verilecek_column.controls.append(temp_buton)
            else:
                temp_buton = ft.ElevatedButton(
                    text=f"Açıklama: {ad}\nVerilecek: {str(-1*int(miktar))}",
                    height=75,
                    width=225,
                    color="red",
                    bgcolor="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),side=ft.BorderSide(width=2, color=ft.Colors.RED)),
                    on_click=lambda e, v=veri: hem_sil_hem_guncelle(v)
                )
                alinacak_column.controls.append(temp_buton)

        ayirici = ft.Row(
            controls=[
                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),

                ft.Text("  Alınacaklar     -     Verilecekler  ", color=ft.Colors.GREY_500, italic=True, weight="bold"),

                ft.Container(height=1, bgcolor=ft.Colors.GREY_700, expand=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )


        sol_adet = len(alinacak_column.controls)
        sag_adet = len(verilecek_column.controls)
        max_adet = max(sol_adet, sag_adet)
        hesaplanan_yukseklik = max(max_adet * 85, 150)


        orta_ayirici = ft.Container(
            width=2,
            height=hesaplanan_yukseklik,
            bgcolor=ft.Colors.GREY_700,
        )


        sol_panel = ft.Container(
            content=verilecek_column,
            expand=1,
            alignment=ft.alignment.top_center
        )


        sag_panel = ft.Container(
            content=alinacak_column,
            expand=1,
            alignment=ft.alignment.top_center
        )


        son_row = ft.Row(
            controls=[sol_panel, orta_ayirici, sag_panel],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0
        )


        page.add(
            ana_row,
            eklekaldir,
            ft.Text(value="\n"),
            ayirici,
            ft.Text(value="\n"),
            son_row,
            konteyner
        )
        page.update()
#----------------------------------------------------------------------------------------------------------------

    def ekran_degistir(e):
        indis = e.control.selected_index

        page.clean()

        if indis == 0:
            duzenli_gelirler_ekrani()
        elif indis == 1:
            duzenli_giderler_ekrani()
        elif indis == 2:
            ana_ekrani()
        elif indis == 3:
            borc_ekrani()

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
            ft.NavigationBarDestination(icon=ft.Icons.MONEY_OFF, label="Düzenli Giderler"),
            ft.NavigationBarDestination(icon=ft.Icons.HOME_ROUNDED, label="Ana Ekran"),
            ft.NavigationBarDestination(icon=ft.Icons.COLLECTIONS_BOOKMARK_ROUNDED, label="Borçlar"),
        ],
        selected_index=1,
        on_change=ekran_degistir

    )

    page.appbar = ust_bar
    page.navigation_bar = alt_bar

    konteyner=ft.Container(height=50)

    guncelpara=page.client_storage.get("guncelpara") or "0"

    def bildirim_goster(mesaj, tur):

        bg_renk = ft.Colors.BLUE_GREY
        ikon = ft.Icons.INFO

        if tur == "olumlu":
            bg_renk = ft.Colors.GREEN_700
            ikon = ft.Icons.CHECK_CIRCLE
        elif tur == "olumsuz":
            bg_renk = ft.Colors.RED_700
            ikon = ft.Icons.ERROR_OUTLINE

        page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ikon, color=ft.Colors.WHITE),
                ft.Text(value=mesaj, color=ft.Colors.WHITE, size=16, weight="bold")
            ]),
            bgcolor=bg_renk,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(20),

            action="Tamam",
            action_color=ft.Colors.WHITE,
            duration=2000,
        )

        page.snack_bar.open = True
        page.update()

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

    def duzenli_gelir_ekle(veri)->bool:

        kontrol=veri["Miktar"]

        try:
            int(kontrol)
        except:
            print("Terminal Girdisi: Hata")
            return False



        mevcut_liste = page.client_storage.get("gelirler_listesi")

        if mevcut_liste is None or not isinstance(mevcut_liste, list):
            mevcut_liste = []

        tur=veri["Tür"]
        ad=veri["Ad"]
        miktar=veri["Miktar"]
        tarih=veri["Tarih"]

        yeni_veri = {"Tür": tur,"Ad": ad, "Miktar": miktar, "Tarih": tarih}


        mevcut_liste.append(yeni_veri)


        page.client_storage.set("gelirler_listesi", mevcut_liste)

        print("Kayıt başarılı!")
        return True

    def duzenli_gelir_ekleme_ekrani(e=None):
        page.clean()
        page.scroll = "auto"

        ad_field = ft.TextField(label="Gelir Adı",border_color=ft.Colors.AMBER)
        miktar_field = ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)


        def onayla_tiklandi(e):

            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Gelir", "Ad": gelen_ad, "Miktar": gelen_miktar, "Tarih": tam_zaman_getir()}

            sonuc=duzenli_gelir_ekle(yeni_veri)


            if sonuc== True:
                duzenli_gelirler_ekrani()
            else:
                print("")

        onayla = ft.ElevatedButton(text="Onayla", color=ft.Colors.AMBER,on_click=onayla_tiklandi,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))

        page.add(
            ft.Text("Yeni Gelir Ekle", size=20,color=ft.Colors.AMBER),
            ad_field,
            miktar_field,
            onayla,
            konteyner,
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
        page.scroll = "auto"
        yeni_liste=page.client_storage.get("gelirler_listesi") or []

        gelir_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
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

        page.add(ana_row, gelir_column, geri_don, konteyner,)
        page.update()

    def duzenli_gelirler_ekrani():
        page.clean()

        page.scroll="auto"

        eslesmeler=page.client_storage.get("gelirler_listesi") or []

        gelir_column=ft.Column(alignment=ft.MainAxisAlignment.START)
        ekle_butonu=ft.ElevatedButton(text="Gelir Ekle",width=150,on_click=duzenli_gelir_ekleme_ekrani,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        kaldir_butonu = ft.ElevatedButton(text="Gelir Kaldır",width=150, on_click=duzenli_gelir_kaldirma_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        butonlar_rowu=ft.Row(controls=[ekle_butonu,kaldir_butonu],alignment=ft.MainAxisAlignment.CENTER)
        for veri in eslesmeler:
            veri["Tarih"]=tam_zaman_getir()
            an=veri["Tarih"]
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

        page.add(ana_row,butonlar_rowu,ft.Text(value="\n"),ayirici,ft.Text(value="\n"),gelir_column,konteyner,)
        page.update()

# ------------------------------------------------------------------------------------------------------------------------

    def log_temizleme(e=None):
        temp=[]
        page.client_storage.set("tum_log", temp)
        ana_ekrani()

    def log_temizle_ekrani(e=None):
        page.clean()
        page.scroll = "auto"
        yazi = ft.Text(value="Geçmişi temizlemek istediğinize emin misiniz?")
        evet = ft.ElevatedButton(text="Evet",color=ft.Colors.AMBER,on_click=log_temizleme,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        hayir = ft.ElevatedButton(text="Hayır",on_click=ana_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        page.add(yazi,evet,hayir,konteyner,)

    def yeni_veri_ekrani_gelir_gider_ekleme(ad,miktar):

        kontrol = miktar

        try:
            int(kontrol)
        except:
            print("Terminal Girdisi: Hata")

            return False

        if int(miktar)<0:
            yeni_veri = {"Tür": "Gider", "Ad": ad, "Miktar": miktar, "Tarih": tam_zaman_getir() }
        else:
            yeni_veri = {"Tür": "Gelir", "Ad": ad, "Miktar": miktar, "Tarih": tam_zaman_getir()}
        guncelpara_degistir(yeni_veri)
        return True

    def yeni_veri_ekrani(e=None):
        page.clean()
        page.scroll = "auto"
        ad_bari=ft.TextField(label="Ad",border_color=ft.Colors.AMBER)
        girdi_bari=ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)
        def islem_yap(ad,miktar):
            sonuc=yeni_veri_ekrani_gelir_gider_ekleme(ad,miktar)
            if sonuc==True:
                ana_ekrani()
            else:
                print("")

        try:
            kontrol=str(-1 * int(girdi_bari.value))
        except:
            print("Terminal Gider: Hata")


        gelir_butonu=ft.ElevatedButton(text="      Gelir      ",on_click=lambda e:islem_yap(ad_bari.value,girdi_bari.value),color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        gider_butonu = ft.ElevatedButton(text="      Gider      ",on_click=lambda e:islem_yap(ad_bari.value,str(-1*int(girdi_bari.value))),color=ft.Colors.RED,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        page.add(
            ad_bari,
            girdi_bari,
            gelir_butonu,
            gider_butonu,
            konteyner
        )
        page.update()

    def guncelpara_sifirla_ekran(e=None):
        page.clean()
        page.scroll = "auto"
        text=ft.Text(value="Sıfırlamak istediğinize emin misiniz?")
        evet = ft.ElevatedButton(text="Evet", on_click=guncelpara_sifirla,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        hayir = ft.ElevatedButton(text="Hayır", on_click=ana_ekrani,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        page.add(
            text,
            evet,
            hayir,
            konteyner
        )
        page.update()


    def guncelpara_sifirla(e=None):
        nonlocal guncelpara
        deger=str(-1*int(guncelpara))
        yeni_veri = {"Tür": "Gider", "Ad": "Sıfırlama İşlemi", "Miktar": deger, "Tarih": tam_zaman_getir()}
        guncelpara_degistir(yeni_veri)
        ana_ekrani()



    def ana_ekrani(e=None):
        page.clean()
        page.scroll = "auto"
        eslesmeler=page.client_storage.get("tum_log") or []


        yeni_veri_ekrani_butonu=ft.ElevatedButton(text="Yeni veri ekle",on_click=yeni_veri_ekrani,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        log_column=ft.Column(alignment=ft.MainAxisAlignment.CENTER)

        para_sifirla=ft.ElevatedButton(text="Bakiye sıfırla...",on_click=guncelpara_sifirla_ekran,color="red",style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))

        for veri in eslesmeler:
            tur=veri["Tür"]
            ad=veri["Ad"]
            miktar=veri["Miktar"]
            an=veri["Tarih"]
            if tur=="Gelir":
                temp=ft.TextField(multiline=True,value=f"Açıklama: {ad}\nMiktar: {miktar}\nTarih: {an}",border_color=ft.Colors.AMBER,read_only=True)
                log_column.controls.append(temp)
            elif tur=="Gider":
                temp = ft.TextField(multiline=True,value=f"Açıklama: {ad}\nMiktar: {miktar}\nTarih: {an}", border_color="red",read_only=True)
                log_column.controls.append(temp)
            elif tur=="Borc":
                if int(miktar)>0:
                    temp = ft.TextField(multiline=True, value=f"Alınan Borç: {ad}\nMiktar: {miktar}\nTarih: {an}",
                                        border_color=ft.Colors.AMBER, read_only=True)
                    log_column.controls.append(temp)
                else:
                    temp = ft.TextField(multiline=True, value=f"Verilen Borç: {ad}\nMiktar: {miktar}\nTarih: {an}",
                                        border_color="red", read_only=True)
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

        log_temizleme_butonu = ft.ElevatedButton(text="Geçmişi Temizle...", on_click=log_temizle_ekrani,color=ft.Colors.LIGHT_BLUE_ACCENT_400, style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.LIGHT_BLUE_ACCENT_700)))

        log_baslangic=temp=ft.TextField(multiline=True,value="Geçmişin Başlangıcı...",border_color=ft.Colors.BLUE_ACCENT_400,read_only=True)
        log_column.controls.append(log_baslangic)
        page.add(
            ana_row,
            butonlar_row,
            log_temizleme_butonu,
            ft.Text(value="\n"),
            ayirici,
            ft.Text(value="\n"),
            log_column,
            konteyner
        )
        page.update()

# ------------------------------------------------------------------------------------------------------------------------

    def log_olustur(veri):
        log=page.client_storage.get("tum_log") or []
        log.append(veri)
        page.client_storage.set("tum_log", log)

# ------------------------------------------------------------------------------------------------------------------------

    def duzenli_gider_ekle(veri) -> bool:

        kontrol = veri["Miktar"]

        try:
            int(kontrol)
        except:
            print("Terminal Girdisi: Hata")
            return False

        mevcut_liste = page.client_storage.get("giderler_listesi")
        if mevcut_liste is None or not isinstance(mevcut_liste, list):
            mevcut_liste = []

        tur=veri["Tür"]
        ad=veri["Ad"]
        miktar=veri["Miktar"]

        yeni_veri = {"Tür": tur,"Ad": ad, "Miktar": str(-1*int(miktar)), "Tarih": tam_zaman_getir()}

        mevcut_liste.append(yeni_veri)
        page.client_storage.set("giderler_listesi", mevcut_liste)

        print("Kayıt başarılı!")
        return True

    def duzenli_gider_ekleme_ekrani(e=None):
        page.clean()
        page.scroll = "auto"
        ad_field = ft.TextField(label="Gider Adı",border_color=ft.Colors.AMBER)
        miktar_field = ft.TextField(label="Miktar",border_color=ft.Colors.AMBER)

        def onayla_tiklandi(e):
            gelen_ad = ad_field.value
            gelen_miktar = miktar_field.value
            yeni_veri = {"Tür": "Gider", "Ad": gelen_ad, "Miktar": gelen_miktar, "Tarih": tam_zaman_getir()}
            sonuc=duzenli_gider_ekle(yeni_veri)

            if sonuc is True:
                duzenli_giderler_ekrani()
            else:
                print("")

        onayla = ft.ElevatedButton(text="Onayla", on_click=onayla_tiklandi,color=ft.Colors.AMBER,style = ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))

        page.add(
            ft.Text("Yeni Gider Ekle", size=20,color=ft.Colors.AMBER),
            ad_field,
            miktar_field,
            onayla,
            konteyner
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
        page.scroll = "auto"
        yeni_liste=page.client_storage.get("giderler_listesi") or []

        gider_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
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

        page.add( ana_row, gider_column, geri_don, konteyner)
        page.update()

    def duzenli_giderler_ekrani():
        page.clean()
        page.scroll = "auto"
        eslesmeler=page.client_storage.get("giderler_listesi") or []

        gider_column=ft.Column(alignment=ft.MainAxisAlignment.START)
        ekle_butonu=ft.ElevatedButton(text="Gider Ekle",width=150,on_click=duzenli_gider_ekleme_ekrani,color=ft.Colors.AMBER,style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.AMBER)))
        kaldir_butonu = ft.ElevatedButton(text="Gider Kaldır",width=150, on_click=duzenli_gider_kaldirma_ekrani,color="red",style=ft.ButtonStyle(side=ft.BorderSide(width=2, color=ft.Colors.RED)))
        butonlar_rowu=ft.Row(controls=[ekle_butonu,kaldir_butonu],alignment=ft.MainAxisAlignment.CENTER)
        for veri in eslesmeler:
            veri["Tarih"] = tam_zaman_getir()
            an = veri["Tarih"]
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
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(ana_row,butonlar_rowu,ft.Text(value="\n"),ayirici,ft.Text(value="\n"),gider_column,konteyner)
        page.update()


    Guncel_Para_Field=ft.TextField(value=f"Güncel Para= {guncelpara}",read_only=True,text_size=20,width=300,height=60,color=ft.Colors.AMBER,border_color=ft.Colors.AMBER_700,border_width=4)
    ana_row=ft.Row(controls=[Guncel_Para_Field],alignment=ft.MainAxisAlignment.CENTER)

    ana_ekrani()



ft.app(target=main, assets_dir="assets")
