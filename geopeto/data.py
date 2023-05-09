from dataclasses import dataclass

import ee

#ee.Initialize()


@dataclass
class GEEData:
    dataset: str

    def image_collection_id(self):
        return {'Global-Land-Cover': 'projects/soils-revealed/ESA_landcover_ipcc',
                'Koppen-Geiger-Climate': ''}[self.dataset]

    def ee_image(self):
        return {'Global-Land-Cover': ee.Image(ee.ImageCollection(self.image_collection_id()).
                                              filterDate('2018-01-01', '2018-12-31').first()),
                'Koppen-Geiger-Climate': ee.Image("users/fsn1995/Global_19862010_KG_5m").updateMask(
                    ee.Image("users/fsn1995/Global_19862010_KG_5m").lte(30))
                }[self.dataset]

    def sld_interval(self):
        return {'Global-Land-Cover': '<RasterSymbolizer>' + '<ColorMap type="values" extended="false">' +
                                     '<ColorMapEntry color="#ffff64" quantity="10" />' +
                                     '<ColorMapEntry color="#ffff64" quantity="11" />' +
                                     '<ColorMapEntry color="#ffff00" quantity="12" />' +
                                     '<ColorMapEntry color="#aaf0f0" quantity="20" />' +
                                     '<ColorMapEntry color="#dcf064" quantity="30" />' +
                                     '<ColorMapEntry color="#c8c864" quantity="40" />' +
                                     '<ColorMapEntry color="#006400" quantity="50" />' +
                                     '<ColorMapEntry color="#00a000" quantity="60" />' +
                                     '<ColorMapEntry color="#00a000" quantity="61" />' +
                                     '<ColorMapEntry color="#aac800" quantity="62" />' +
                                     '<ColorMapEntry color="#003c00" quantity="70" />' +
                                     '<ColorMapEntry color="#003c00" quantity="71" />' +
                                     '<ColorMapEntry color="#005000" quantity="72" />' +
                                     '<ColorMapEntry color="#285000" quantity="80" />' +
                                     '<ColorMapEntry color="#285000" quantity="81" />' +
                                     '<ColorMapEntry color="#286400" quantity="82" />' +
                                     '<ColorMapEntry color="#788200" quantity="90" />' +
                                     '<ColorMapEntry color="#8ca000" quantity="100" />' +
                                     '<ColorMapEntry color="#be9600" quantity="110" />' +
                                     '<ColorMapEntry color="#966400" quantity="120" />' +
                                     '<ColorMapEntry color="#966400" quantity="121" />' +
                                     '<ColorMapEntry color="#966400" quantity="122" />' +
                                     '<ColorMapEntry color="#ffb432" quantity="130" />' +
                                     '<ColorMapEntry color="#ffdcd2" quantity="140" />' +
                                     '<ColorMapEntry color="#ffebaf" quantity="150" />' +
                                     '<ColorMapEntry color="#ffc864" quantity="151" />' +
                                     '<ColorMapEntry color="#ffd278" quantity="152" />' +
                                     '<ColorMapEntry color="#ffebaf" quantity="153" />' +
                                     '<ColorMapEntry color="#00785a" quantity="160" />' +
                                     '<ColorMapEntry color="#009678" quantity="170" />' +
                                     '<ColorMapEntry color="#00dc82" quantity="180" />' +
                                     '<ColorMapEntry color="#c31400" quantity="190" />' +
                                     '<ColorMapEntry color="#fff5d7" quantity="200" />' +
                                     '<ColorMapEntry color="#dcdcdc" quantity="201" />' +
                                     '<ColorMapEntry color="#fff5d7" quantity="202" />' +
                                     '<ColorMapEntry color="#0046c8" quantity="210" opacity="0" />' +
                                     '<ColorMapEntry color="#ffffff" quantity="220" />' +
                                     '</ColorMap>' + '</RasterSymbolizer>',
                'Koppen-Geiger-Climate': '<RasterSymbolizer>' +
                                         '<ColorMap type="values" extended="false">' +
                                         '<ColorMapEntry color="#960000" quantity="0" />' +
                                         '<ColorMapEntry color="#FF0000" quantity="1" />' +
                                         '<ColorMapEntry color="#FF6E6E" quantity="2" />' +
                                         '<ColorMapEntry color="#FFCCCC" quantity="3" />' +
                                         '<ColorMapEntry color="#CC8D14" quantity="4" />' +
                                         '<ColorMapEntry color="#CCAA54" quantity="5" />' +
                                         '<ColorMapEntry color="#FFCC00" quantity="6" />' +
                                         '<ColorMapEntry color="#FFFF64" quantity="7" />' +
                                         '<ColorMapEntry color="#007800" quantity="8" />' +
                                         '<ColorMapEntry color="#005000" quantity="9" />' +
                                         '<ColorMapEntry color="#003200" quantity="10" />' +
                                         '<ColorMapEntry color="#96FF00" quantity="11" />' +
                                         '<ColorMapEntry color="#00D700" quantity="12" />' +
                                         '<ColorMapEntry color="#00AA00" quantity="13" />' +
                                         '<ColorMapEntry color="#BEBE00" quantity="14" />' +
                                         '<ColorMapEntry color="#8C8C00" quantity="15" />' +
                                         '<ColorMapEntry color="#5A5A00" quantity="16" />' +
                                         '<ColorMapEntry color="#550055" quantity="17" />' +
                                         '<ColorMapEntry color="#820082" quantity="18" />' +
                                         '<ColorMapEntry color="#C800C8" quantity="19" />' +
                                         '<ColorMapEntry color="#FF6EFF" quantity="20" />' +
                                         '<ColorMapEntry color="#646464" quantity="21" />' +
                                         '<ColorMapEntry color="#8C8C8C" quantity="22" />' +
                                         '<ColorMapEntry color="#BEBEBE" quantity="23" />' +
                                         '<ColorMapEntry color="#E6E6E6" quantity="24" />' +
                                         '<ColorMapEntry color="#6E28B4" quantity="25" />' +
                                         '<ColorMapEntry color="#B464FA" quantity="26" />' +
                                         '<ColorMapEntry color="#C89BFA" quantity="27" />' +
                                         '<ColorMapEntry color="#C8C8FF" quantity="28" />' +
                                         '<ColorMapEntry color="#6496FF" quantity="29" />' +
                                         '<ColorMapEntry color="#64FFFF" quantity="30" />' +
                                         '<ColorMapEntry color="#F5FFFF" quantity="31" />' +
                                         '</ColorMap>' + '</RasterSymbolizer>'
                }[self.dataset]

    def class_colors(self):
        return {'Global-Land-Cover': {"10": "#ffff64", "11": "#ffff64", "12": "#ffff00", "20": "#aaf0f0",
                                      "30": "#dcf064", "40": "#c8c864", "50": "#006400", "60": "#00a000",
                                      "61": "#00a000", "62": "#aac800", "70": "#003c00", "71": "#003c00",
                                      "72": "#005000", "80": "#285000", "81": "#285000", "82": "#286400",
                                      "90": "#788200", "100": "#8ca000", "110": "#be9600", "120": "#966400",
                                      "121": "#966400", "122": "#966400", "130": "#ffb432", "140": "#ffdcd2",
                                      "150": "#ffebaf", "151": "#ffc864", "152": "#ffd278", "153": "#ffebaf",
                                      "160": "#00785a", "170": "#009678", "180": "#00dc82", "190": "#c31400",
                                      "200": "#fff5d7", "201": "#dcdcdc", "202": "#fff5d7", "210": "#0046c8",
                                      "220": "#ffffff"},
                'Koppen-Geiger-Climate': {'0': '#960000', '1': '#FF0000', '2': '#FF6E6E', '3': '#FFCCCC',
                                          '4': '#CC8D14', '5': '#CCAA54', '6': '#FFCC00', '7': '#FFFF64',
                                          '8': '#007800', '9': '#005000', '10': '#003200', '11': '#96FF00',
                                          '12': '#00D700', '13': '#00AA00', '14': '#BEBE00', '15': '#8C8C00',
                                          '16': '#5A5A00', '17': '#550055', '18': '#820082', '19': '#C800C8',
                                          '20': '#FF6EFF', '21': '#646464', '22': '#8C8C8C', '23': '#BEBEBE',
                                          '24': '#E6E6E6', '25': '#6E28B4', '26': '#B464FA', '27': '#C89BFA',
                                          '28': '#C8C8FF', '29': '#6496FF', '30': '#64FFFF'}
                }[self.dataset]

    def class_names(self):
        return {'Global-Land-Cover': {"10": "Cropland, rainfed",
                                      "11": "Cropland, rainfed, herbaceous cover",
                                      "12": "Cropland, rainfed, tree, or shrub cover",
                                      "20": "Cropland, irrigated or post-flooding",
                                      "30": "Mosaic cropland (>50%) / natural vegetation (tree, shrub, herbaceous cover) (<50%)",
                                      "40": "Mosaic natural vegetation (tree, shrub, herbaceous cover) (>50%) / cropland (<50%)",
                                      "50": "Tree cover, broadleaved, evergreen, closed to open (>15%)",
                                      "60": "Tree cover, broadleaved, deciduous, closed to open (>15%)",
                                      "61": "Tree cover, broadleaved, deciduous, closed (>40%)",
                                      "62": "Tree cover, broadleaved, deciduous, open (15- 40%)",
                                      "70": "Tree cover, needleleaved, evergreen, closed to open (>15%)",
                                      "71": "Tree cover, needleleaved, evergreen, closed (>40%)",
                                      "72": "Tree cover, needleleaved, evergreen, open (15-40%)",
                                      "80": "Tree cover, needleleaved, deciduous, closed to open (>15%)",
                                      "81": "Tree cover, needleleaved, deciduous, closed (>40%)",
                                      "82": "Tree cover, needleleaved, deciduous, open (15-40%)",
                                      "90": "Tree cover, mixed leaf type (broadleaved and needleleaved)",
                                      "100": "Mosaic tree and shrub (>50%) / herbaceous cover (<50%)",
                                      "110": "Mosaic herbaceous cover (>50%) / tree and shrub (<50%)",
                                      "120": "Shrubland",
                                      "121": "Evergreen shrubland",
                                      "122": "Deciduous shrubland",
                                      "130": "Grassland",
                                      "140": "Lichens and mosses",
                                      "150": "Sparse vegetation (tree, shrub, herbaceous cover) (<15%)",
                                      "151": "Sparse tree (<15%)",
                                      "152": "Sparse shrub (<15%)",
                                      "153": "Sparse herbaceous cover (<15%)",
                                      "160": "Tree cover, flooded, fresh, or brackish water",
                                      "170": "Tree cover, flooded, saline water",
                                      "180": "Shrub or herbaceous cover, flooded, fresh/saline/brackish water",
                                      "190": "Urban areas",
                                      "200": "Bare areas ",
                                      "201": "Consolidated bare areas",
                                      "202": "Unconsolidated bare areas",
                                      "210": "Water bodies",
                                      "220": "Permanent snow and ice "},
                'Koppen-Geiger-Climate': {'0': 'Tropical rainforest climate',
                                          '1': 'Tropical monsoon climate',
                                          '2': 'Tropical wet and dry or savanna climate',
                                          '3': 'Tropical wet and dry or savanna climate',
                                          '4': 'Hot semi-arid climate',
                                          '5': 'Cold semi-arid climate',
                                          '6': 'Hot desert climate',
                                          '7': 'Cold desert climate',
                                          '8': 'Humid subtropical climate',
                                          '9': 'Temperate oceanic climate or subtropical highland climate',
                                          '10': 'Subpolar oceanic climate',
                                          '11': 'Hot-summer Mediterranean climate',
                                          '12': 'Warm-summer Mediterranean climate',
                                          '13': 'Cold-summer Mediterranean climate',
                                          '14': 'Monsoon-influenced humid subtropical climate',
                                          '15': 'Subtropical highland climate or Monsoon-influenced temperate oceanic climate',
                                          '16': 'Cold subtropical highland climate or Monsoon-influenced subpolar oceanic climate',
                                          '17': 'Hot-summer humid continental climate',
                                          '18': 'Warm-summer humid continental climate',
                                          '19': 'Subarctic climate',
                                          '20': 'Extremely cold subarctic climate',
                                          '21': 'Mediterranean-influenced hot-summer humid continental climate',
                                          '22': 'Mediterranean-influenced warm-summer humid continental climate',
                                          '23': 'Mediterranean-influenced subarctic climate',
                                          '24': 'Mediterranean-influenced extremely cold subarctic climate',
                                          '25': 'Monsoon-influenced hot-summer humid continental climate',
                                          '26': 'Monsoon-influenced warm-summer humid continental climate',
                                          '27': 'Monsoon-influenced subarctic climate',
                                          '28': 'Monsoon-influenced extremely cold subarctic climate',
                                          '29': 'Ice cap climate',
                                          '30': 'Tundra climate'}
                }[self.dataset]