INTERVALO_SEGUNDOS = 5 * 60
PORTA_PAINEL = 8050
MAX_THREADS = 8
TIMEOUT = 15

TRECHOS_MOTIVA = {
    "Fernão Dias (BR-381) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=internal&id=minas_sp_br381_sul_norte&type=single&concessionId=minassp&services=Toll,%20EletronicToll,%20SAU,%20TruckDriverRestStation,%20PoliceStation"
    ),
    "Fernão Dias (BR-381) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=internal&id=minas_sp_br381_norte_sul&type=single&concessionId=minassp&services=Toll,%20EletronicToll,%20SAU,%20TruckDriverRestStation,%20PoliceStation"
    ),
    "Anhanguera (SP-330) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=autoban_sp330&origin=139&destination=1&concessionId=autoban&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Anhanguera (SP-330) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=autoban_sp330&origin=139&destination=1&concessionId=autoban&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Bandeirantes (SP-348) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=autoban_sp348&origin=1&destination=139&concessionId=autoban&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Bandeirantes (SP-348) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=autoban_sp348&origin=1&destination=139&concessionId=autoban&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Rodovia do Café (BR-376/PR) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=prvias_br376&origin=291&destination=281&concessionId=prvias&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Rodovia do Café (BR-376/PR) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=prvias_br376&origin=281&destination=291&concessionId=prvias&services=Toll,%20EletronicToll,%20CustomsStation,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Dutra (BR-116) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=riosp_br116&origin=29&destination=1&concessionId=riosp&services=Toll,%20EletronicToll,%20SAU,%20FreeFlowDynamic,%20TruckDriverRestStation,%20PoliceStation"
    ),
    "Dutra (BR-116) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=riosp_br116&origin=1&destination=29&concessionId=riosp&services=Toll,%20EletronicToll,%20SAU,%20FreeFlowDynamic,%20TruckDriverRestStation,%20PoliceStation"
    ),
    "Mário Covas SC (BR-101) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=internal&id=viacosteira_br101sc_sul_norte&type=single&concessionId=viacosteira&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Mário Covas SC (BR-101) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=viacosteira_br101sc&origin=68&destination=67&concessionId=viacosteira&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Mário Covas RS (BR-101) - Sentido Norte": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=viasul_br101&origin=85&destination=91&concessionId=viasul&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Mário Covas RS (BR-101) - Sentido Sul": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=viasul_br101&origin=91&destination=85&concessionId=viasul&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Freeway Oswaldo Aranha (BR-290) - Sentido Leste": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=viasul_br290&origin=92&destination=85&concessionId=viasul&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
    "Freeway Oswaldo Aranha (BR-290) - Sentido Oeste": (
        "https://rodovias.motiva.com.br/bin/mapConcession/?action=segment&id=viasul_br290&origin=85&destination=92&concessionId=viasul&services=Toll,%20EletronicToll,%20PoliceStation,%20SAU,%20TruckDriverRestStation"
    ),
}
CABECALHOS_MOTIVA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://rodovias.motiva.com.br/",
}
TRECHOS_ARTERIS = {
    "Regis Bittencourt (BR-116)": "https://www.arteris.com.br/api/mapa-interativo/regis_bittencourt/trecho/53/133/",
    "Litoral Sul (BR-116/376/101)": "https://www.arteris.com.br/api/mapa-interativo/litoral_sul/trecho/50/77/",
}
CABECALHOS_ARTERIS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.arteris.com.br/",
}