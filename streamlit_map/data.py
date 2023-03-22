from dataclasses import dataclass

import ee

ee.Initialize()


@dataclass
class GEEData:
    dataset: str

    def image_collection_id(self):
        return {'Global-Land-Cover': 'projects/soils-revealed/ESA_landcover_ipcc'}[self.dataset]

    def ee_image(self):
        return {'Global-Land-Cover': ee.Image(ee.ImageCollection(self.image_collection_id()).
                                              filterDate('2018-01-01', '2018-12-31').first())}[self.dataset]

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
                                      "220": "#ffffff"}
                }[self.dataset]
