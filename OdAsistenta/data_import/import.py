import json
import csv
from pyproj import Transformer
from elasticsearch import Elasticsearch

# settings
DEBUG = False
DEBUG_SIZE = 100

# clear and init indexes for es
es = Elasticsearch()
es.indices.delete(index='house', ignore=[400, 404])
with open('data_import/data_minimal.json', 'r') as f:
    es_mappings = json.loads(f.read())
    es.indices.create(index='house', body=es_mappings)

# init coordinates transformer
transformer = Transformer.from_crs("EPSG:3794", "EPSG:4326")


def read_csv(filename, root_key='STA_SID', as_list=False):
    with open(filename, 'r') as f:
        c = list(csv.reader(f, delimiter=';'))
        keys, c = c[0], c[1:]

        root_key_index = keys.index(root_key)
        if root_key_index == -1: raise

        data = {}

        for line in c:
            d = {}
            for i in range(len(keys)):
                d[keys[i]] = line[i]

            if as_list:
                if line[root_key_index] in data:
                    data[line[root_key_index]].append(d)
                else:
                    data[line[root_key_index]] = [d]
            else:
                data[line[root_key_index]] = d

        return data


def translate(uid):
    try:
        return sifranti_id[uid]['IME']
    except:
        return None


STAVBE_FILENAME = 'data/REN_SLO_stavbe_20190923.csv'
PAR_FILENAME = 'data/REN_SLO_sta_par_20190923.csv'
SESTAVINE_FILENAME = 'data/REN_SLO_sestavine_20190923.csv'
DELISTAVB_FILENAME = 'data/REN_SLO_delistavb_20190923.csv'
SIFRANTI_FILENAME = 'data/REN_SLO_sifranti_20190923.csv'
NRABA_FILENAME = 'data/REN_SLO_nraba_parcele_20190923.csv'
DRABA_FILENAME = 'data/REN_SLO_draba_parcele_20190923.csv'
GARAZA_FILENAME = 'data/REN_SLO_garaza_20190923.csv'
IZOLACIJA_FILENAME = 'data/REN_SLO_izolacija_20190923.csv'
MODELI_DST_FILENAME = 'data/REN_SLO_modeli_dst_20190923.csv'
MODELI_PARC_FILENAME = 'data/REN_SLO_modeli_parc_20190923.csv'
LASTNIKI_PRAV_FILENAME = 'data/REN_SLO_lastniki_prav_20190923.csv'
PARCELE_FILENAME = 'data/REN_SLO_parcele_20190923.csv'
POSEBNE_DELISTAVB_FILENAME = 'data/REN_SLO_posebne_delistavb_20190923.csv'
POSEBNE_PARCELE_FILENAME = 'data/REN_SLO_posebne_parcele_20190923.csv'
PROSTORI_FILENAME = 'data/REN_SLO_prostori_20190923.csv'
NASLOVI_FILENAME = 'data/REN_SLO_stavba_naslovi_20190923.csv'
UPRAVLJAVCI_FILENAME = 'data/REN_SLO_upravljavci_20190923.csv'

print('loading data')
stavbe = read_csv(STAVBE_FILENAME)
print('loaded stavbe')
pari = read_csv(PAR_FILENAME)
print('loaded pari')
sestavine_pc_mid = read_csv(SESTAVINE_FILENAME, root_key='PC_MID')
print('loaded sestavine_parcele')
sestavine_dst_sid = read_csv(SESTAVINE_FILENAME, root_key='DST_SID')
print('loaded sestavine_deli_stanovanj')
delistavb = read_csv(DELISTAVB_FILENAME, as_list=True)
print('loaded delistavb')
sifranti_id = read_csv(SIFRANTI_FILENAME, root_key='ID')
print('loaded sifranti')
# garaze = read_csv(GARAZA_FILENAME, root_key='DST_SID')
# print('loaded garaze')
draba = read_csv(DRABA_FILENAME, root_key='PC_MID')
print('loaded draba')
nraba = read_csv(NRABA_FILENAME, root_key='PC_MID')
print('loaded nraba')
# modeli_dst = read_csv(MODELI_DST_FILENAME, root_key='DST_SID', as_list=True)
# print('loaded modeli_dst')
# modeli_parc = read_csv(MODELI_PARC_FILENAME, root_key='PC_MID', as_list=True)
# print('loaded modeli_parc')
# lastniki_prav = read_csv(LASTNIKI_PRAV_FILENAME, root_key='NEN_ID', as_list=True)
# print('loaded lastniki_prav')
# izolacije = read_csv(IZOLACIJA_FILENAME, root_key='DST_SID')
# print('loaded izolacije')
parcele = read_csv(PARCELE_FILENAME, root_key='PC_MID')
print('loaded parcele')
# posebne_delistavb = read_csv(POSEBNE_DELISTAVB_FILENAME, root_key='DST_SID')
# print('loaded posebne_delistavb')
# posebne_parcele = read_csv(POSEBNE_PARCELE_FILENAME, root_key='PC_MID')
# print('loaded posebne_parcele')
# prostori = read_csv(PROSTORI_FILENAME, root_key='DST_SID', as_list=True)
# print('loaded prostori')
# naslovi = read_csv(NASLOVI_FILENAME)
# print('loaded naslovi')
# upravljavci = read_csv(UPRAVLJAVCI_FILENAME, root_key='NEN_ID')
# print('loaded upravljalci')

size = len(stavbe.keys())

for i, sta_sid in enumerate(stavbe.keys()):
    # id
    stavba = stavbe[sta_sid]
    ob_mid = stavba['OB_MID']

    # tip stavbe
    tip_stavbe = translate(stavba['ID_TIP_STAVBE'])

    # lokacija
    x, y = stavba['CEN_N'], stavba['CEN_E']
    x = x.replace(',', '.')
    y = y.replace(',', '.')
    lat, lon = transformer.transform(y, x)

    # konstrukcija, ogrevanje, vodovod, elektrika, kanalizacija, plin, kabelska, temeljenje, tehnicni pin, idnutrijski tok, kompresiran zrak, cistilna naprava
    # konstrukcija = translate(stavba['ID_KONSTRUKCIJE'])
    # ogrevanje = translate(stavba['ID_OGREVANJE'])
    # vodovod = translate(stavba['ID_VODOVOD'])
    # elektrika = translate(stavba['ID_ELEKTRIKA'])
    # kanalizacija = translate(stavba['ID_KANALIZACIJA'])
    # plin = translate(stavba['ID_PLIN'])
    # kabelska = translate(stavba['ID_KABELSKA_TV'])
    # temeljenje = translate(stavba['ID_TEMELJENJE'])
    # teh_plin = translate(stavba['ID_TEH_PLIN'])
    # ind_tok = translate(stavba['ID_IND_TOK'])
    # komp_zrak = translate(stavba['ID_KOMP_ZRAK'])
    # cistilna_naprava = translate(stavba['ID_CIST_NAPRAVA'])

    if sta_sid not in delistavb:
        # obstajata 2 stavbi, ki nimata delov - ker sta samo dve, ju izpustimo TODO: ugotovit zakaj ju ni
        continue

    # deli stavbe
    deli = []
    for del_stavbe in delistavb[sta_sid]:
        dst_sid = del_stavbe['DST_SID']
        nen_id = sestavine_dst_sid[dst_sid]['NEN_ID']

        vrednost = float(sestavine_dst_sid[dst_sid]['VREDNOST_SEST'].replace(',', '.')) if sestavine_dst_sid[dst_sid][
                                                                                               'VREDNOST_SEST'] != '' else None

        # vrsta_parkirnega_prostora = None
        # stevilo_parkirnih_mest = None
        # if dst_sid in garaze:
        #     vrsta_parkirnega_prostora = translate(garaze[dst_sid]['ID_VRSTA'])
        #     stevilo_parkirnih_mest = int(garaze[dst_sid]['ST_PARMES']) if garaze[dst_sid]['ST_PARMES'] != '' else None

        # modeli = []
        # if sta_sid in modeli_dst:
        #     for model in modeli_dst[sta_sid]:
        #         modeli.append({
        #             'model_ocenjevanja': model['ID_MODEL'],
        #             'raven_ocenjevanja': model['RAVEN'],
        #             'vrednost_po_modelu': float(model['VREDNOST'].replace(',', '.')) if model[
        #                                                                                     'VREDNOST'] != '' else None,
        #             'vplivno_obmocje': model['VPLIV']
        #         })

        # lastniki
        # lastniki = []
        # if nen_id in lastniki_prav:
        #     for lastnik in lastniki_prav[nen_id]:
        #         lastniki.append({
        #             'lastnik_emso_ms': lastnik['EMSO_MS'],
        #             'lastnik_ime': lastnik['IME'],
        #             'lastnik_naslov': lastnik['NASLOV'],
        #             'lastnik_leto_rojstva': lastnik['LETO'],
        #             'delez_lastnistva_stevec': lastnik['DELEZ_STEV_IZR'],
        #             'delez_lastnistva_imenovalec': lastnik['DELEZ_IMEN_IZR']
        #         })

        # upravljavec_emso_ms = None
        # upravljavec_ime = None
        # upravljavec_naslov = None
        # upravljavec_status = None
        # if nen_id in upravljavci:
        #     upravljavec_emso_ms = upravljavci[nen_id]['EMSO_MS']
        #     upravljavec_ime = upravljavci[nen_id]['IME']
        #     upravljavec_naslov = upravljavci[nen_id]['NASLOV']
        #     upravljavec_status = 'zacasni' if upravljavci[nen_id]['STAT_UPR'].lower() == 'z' else 'dokoncni'
        #
        # naziv_posebnosti_dela_stavbe = None
        # if dst_sid in posebne_delistavb:
        #     naziv_posebnosti_dela_stavbe = posebne_delistavb[dst_sid]['NAZIV']

        # prostori
        # prostori = []
        # if dst_sid in prostori:
        #     for prostor in prostori[dst_sid]:
        #         prostori.append({
        #             'tip_prostora': translate(prostor['ID_PROSTORA']),
        #             'povrsina': float(prostor['POVRSINA'].replace(',', '.')) if prostor['POVRSINA'] != '' else None
        #         })

        d = {
            # 'stevilka_dela_stavbe': int(del_stavbe['STEVDST']) if del_stavbe['STEVDST'] != '' else None,
            # 'stevilka_stanovanja': int(del_stavbe['STEVSTAN']) if del_stavbe['STEVSTAN'] != '' else None,
            'stevilka_etaze': int(del_stavbe['ST_ETAZE']) if del_stavbe['ST_ETAZE'] != '' else None,
            'stevilka_nadstropj': int(del_stavbe['ST_NADSTROPJA']) if del_stavbe['ST_NADSTROPJA'] != '' else None,
            # 'katastrski_vpis': del_stavbe['KATAS_VPIS'],
            'dejanska_raba': translate(del_stavbe['DEJANSKA_RABA']),
            # 'vrednost': vrednost,
            'uporabna_povrsina_stanovanja': float(del_stavbe['UPOR_POV_STAN'].replace(',', '.')) if del_stavbe[
                                                                                                        'UPOR_POV_STAN'] != '' else None,
            'neto_tloris_povrsina_dela_stavbe': float(del_stavbe['NETO_TLORIS_POV_DST'].replace(',', '.')) if
            del_stavbe['NETO_TLORIS_POV_DST'] != '' else None,
            # 'leto_obnove_oken': int(del_stavbe['LETO_OBN_OKEN']) if del_stavbe['LETO_OBN_OKEN'] != '' else None,
            # 'leto_obnove_instalacij': int(del_stavbe['LETO_OBN_INST']) if del_stavbe['LETO_OBN_INST'] != '' else None,
            # 'maticna_stevilka_upravnika': del_stavbe['MS_UPRAVNIKA'],
            'lega_v_stavbi': translate(del_stavbe['ID_LEGA']),
            # 'kuhinja': translate(del_stavbe['ID_KUHINJA']),
            # 'kopalnica': translate(del_stavbe['ID_KOPALNICA']),
            # 'stranisce': translate(del_stavbe['ID_STRANISCE']),
            # 'stevilo_sob': int(del_stavbe['ST_SOB']) if del_stavbe['ST_SOB'] != '' else None,
            # 'klima': translate(del_stavbe['ID_KLIMA']),
            # 'pocitniska_raba': translate(del_stavbe['ID_POCIT_RABA']),
            # 'opravljanje_dejavnosti': translate(del_stavbe['ID_PRIJAVA_DEJAV']),
            # 'stevilo_sob_dejavnost': int(del_stavbe['ST_SOB_DEJAVNOST']) if del_stavbe[
            #                                                                     'ST_SOB_DEJAVNOST'] != '' else None,
            # 'povrsina_sob_dejavnost': float(del_stavbe['ST_SOB_DEJAVNOST']) if del_stavbe[
            #                                                                        'ST_SOB_DEJAVNOST'] != '' else None,
            # 'talne_obloge': translate(del_stavbe['ID_TALNE_OBLOGE']),
            # 'obdelava_stropa': translate(del_stavbe['ID_OBDELAVA_STROPA']),
            # 'izlozbeno_okno': translate(del_stavbe['ID_IZLOZBENO_OKNO']),
            # 'vhod_z_ulice': translate(del_stavbe['ID_VHOD_ULICA']),
            # 'visina_etaze': float(del_stavbe['SVETLA_VISINA_ETAZE'].replace(',', '.')) if del_stavbe[
            #                                                                                   'SVETLA_VISINA_ETAZE'] != '' else None,
            # 'razdalja_med_nosilnimi_elementi': float(del_stavbe['RAZDALJA_MED_ELTI'].replace(',', '.')) if del_stavbe[
            #                                                                                                    'RAZDALJA_MED_ELTI'] != '' else None,
            # 'prostornina': float(del_stavbe['PROSTORNINA'].replace(',', '.')) if del_stavbe[
            #                                                                          'PROSTORNINA'] != '' else None,
            # 'dve_ali_vec_etaz': translate(del_stavbe['ID_DUPLEX']),
            # 'dvigalo': translate(del_stavbe['ID_DVIGALO']),
            # 'vrsta_parkirnega_prostora': vrsta_parkirnega_prostora,
            # 'stevilo_parkirnih_mest': stevilo_parkirnih_mest,
            # 'modeli_ocenjevanja': modeli,
            # 'lastniki': lastniki,
            # 'izolacija': translate(izolacije[dst_sid]['ID_IZOLACIJE']) if dst_sid in izolacije else None,
            # 'naziv_posebnosti_dela_stavbe': 'naziv_posebnosti_dela_stavbe',
            # 'prostori': prostori,
            # 'upravljavec_emso_ms': upravljavec_emso_ms,
            # 'upravljavec_ime': upravljavec_ime,
            # 'upravljavec_naslov': upravljavec_naslov,
            # 'upravljavec_status': upravljavec_status,
        }
        deli.append(d)

    povrsina_pod_stavbo = None
    vrednost_parcele = None
    dejanska_raba_parcele = None
    delez_dejanske_rabe = None
    namenska_raba_parcele = None
    delez_namenske_rabe = None
    # odprtost_zemljisca = None
    # rastiscni_koeficient = None
    # stevilka_parcele = None
    povrsina_parcele = None
    # lat_parcele, lon_parcele = None, None
    # boniteta_parcele = None
    # modeli = []
    # naziv_posebnosti_parcele = None
    # delez_posebnosti_parcele = None
    if sta_sid in pari:
        pc_mid = pari[sta_sid]['PC_MID']
        povrsina_pod_stavbo = pari[sta_sid]['POVRSINA']
        vrednost_parcele = float(sestavine_pc_mid[pc_mid]['VREDNOST_SEST'].replace(',', '.')) if \
            sestavine_pc_mid[pc_mid]['VREDNOST_SEST'] != '' else None

        if pc_mid in draba:
            dejanska_raba_parcele = translate(draba[pc_mid]['D_RABA'])
            delez_dejanske_rabe = float(draba[pc_mid]['DELEZ_DR'].replace(',', '.')) / 100 if draba[pc_mid][
                                                                                                  'DELEZ_DR'] != '' else None

        if pc_mid in nraba:
            namenska_raba_parcele = translate(nraba[pc_mid]['N_RABA'])
            delez_namenske_rabe = float(nraba[pc_mid]['DELEZ'].replace(',', '.')) / 100 if nraba[pc_mid][
                                                                                               'DELEZ'] != '' else None
            # odprtost_zemljisca = nraba[pc_mid]['ODPRTOST']
            # rastiscni_koeficient = nraba[pc_mid]['RK']

        # modeli ocenjevanja
        # if pc_mid in modeli_parc:
        #     for model in modeli_parc[pc_mid]:
        #         modeli.append({
        #             'model_ocenjevanja': model['ID_MODEL'],
        #             'ime_vrednostne_cone': model['CONA_IME'],
        #             'raven_ocenjevanja': model['RAVEN'],
        #             'delez_povrsine': float(model['DELEZ_POV'].replace(',', '.')) / 100 if model[
        #                                                                                        'DELEZ_POV'] != '' else None,
        #             'vrednost': float(model['VREDNOST'].replace(',', '.')) if model['VREDNOST'] != '' else None,
        #             'delez_namenske_rabe': float(model['DELEZ_NAMENSKE'].replace(',', '.')) / 100 if model[
        #                                                                                                  'VREDNOST'] != '' else None,
        #             'delez_dejanske_rabe': float(model['DELEZ_DEJANSKE'].replace(',', '.')) / 100 if model[
        #                                                                                                  'VREDNOST'] != '' else None,
        #             'vpliv': model['VPLIV']
        #         })

        # podatki o parceli
        stevilka_parcele = parcele[pc_mid]['PARCELA']
        povrsina_parcele = parcele[pc_mid]['POVRSINA']
        # x_parcele, y_parcele = parcele[pc_mid]['CEN_N'], parcele[pc_mid]['CEN_E']
        # x_parcele = x_parcele.replace(',', '.')
        # y_parcele = y_parcele.replace(',', '.')
        # lat_parcele, lon_parcele = transformer.transform(y, x)
        # boniteta_parcele = float(parcele[pc_mid]['BONITETA'].replace(',', '.')) if parcele[pc_mid][
        #                                                                                'BONITETA'] != '' else None

        # posebnosti
        # if pc_mid in posebne_parcele:
        #     naziv_posebnosti_parcele = posebne_parcele[pc_mid]['NAZIV']
        #     delez_posebnosti_parcele = posebne_parcele[pc_mid]['DELEZ']

    new = {
        # 'enolicni_identifikator_stavbe': sta_sid,
        # 'sifra_katastrske_obcine': stavba['KO_SIFKO'],
        # 'stevilka_stavbe': stavba['STEV'],
        # 'enolicni_identifikator_obcine': stavba['OB_MID'],
        # 'katastrski_vpis': stavba['KATAS_VPIS'] == '1',
        'stevilo_etaz': int(stavba['ST_ETAZ']) if stavba['ST_ETAZ'] != '' else None,
        # 'stevilka_pritlicne_etaze': int(stavba['ST_PRIT_ETAZE']) if stavba['ST_PRIT_ETAZE'] != '' else None,
        'stevilo_stanovanj': int(stavba['ST_STANOVANJ']),
        # 'stevilo_poslovnih_prostorov': int(stavba['ST_POSLOVNIH_PROSTOROV']),
        'tip_stavbe': tip_stavbe,
        'leto_izgradnje_stavbe': int(stavba['LETO_IZG_STA']) if stavba['LETO_IZG_STA'] != '' else None,
        # 'leto_obnove_strehe': int(stavba['LETO_OBN_STREHE']) if stavba['LETO_OBN_STREHE'] != '' else None,
        # 'leto_obnove_fasade': int(stavba['LETO_OBN_FASADE']) if stavba['LETO_OBN_FASADE'] != '' else None,
        'location': {
            "lat": lat,
            "lon": lon
        },
        # 'konstrukcija': konstrukcija,
        # 'ogrevanje': ogrevanje,
        # 'vodovod': vodovod,
        # 'elektrika': elektrika,
        # 'kanalizacija': kanalizacija,
        # 'plin': plin,
        # 'kabelska': kabelska,
        # 'temeljenje': temeljenje,
        # 'teh_plin': teh_plin,
        # 'ind_tok': ind_tok,
        # 'komprimiran_zrak': komp_zrak,
        # 'cistilna_naprava': cistilna_naprava,
        'deli': deli,
        'povrsina_pod_stavbo': povrsina_pod_stavbo,
        'dejanska_raba_parcele': dejanska_raba_parcele,
        'delez_dejanske_rabe': delez_dejanske_rabe,
        'namenska_raba_parcele': namenska_raba_parcele,
        'delez_namenske_rabe': delez_namenske_rabe,
        # 'odprtost_zemljisca': odprtost_zemljisca,
        # 'rastiscni_koeficient': rastiscni_koeficient,
        # 'modeli_ocenjevanja': modeli,
        # 'stevilka_parcele': stevilka_parcele,
        'povrsina_parcele': povrsina_parcele,
        # 'boniteta_parcele': boniteta_parcele,
        # 'naziv_posebnosti_parcele': naziv_posebnosti_parcele,
        # 'delez_posebnosti_parcele': delez_posebnosti_parcele,
        # 'naslov_hs_mid': naslovi[sta_sid] if sta_sid in naslovi else None,
    }

    # if lat_parcele is not None and lon_parcele is not None:
    #    new['lokacija_parcele'] = {
    #        "lat": lat_parcele,
    #        "lon": lon_parcele
    #    }

    es.index(index='house', id=i, body=new)

    if i % 100 == 0:
        part = i / size
        print('\rcomputing [{}{}] {:.2f} %'.format('#' * round(100 * part), '.' * round(100 * (1 - part)), 100 * part),
              end='')

# print 100%
part = 1.0
print('\rcomputing [{}{}] {:.2f} %'.format('#' * round(100 * part), '.' * round(100 * (1 - part)), 100 * part), end='')

print()
print('done')
