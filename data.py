from dataclasses import dataclass


@dataclass
class GEEData:
    dataset: str

    def asset_id(self):
        return {'Current-SOC-stocks-(0-200-cm)': 'users/iker/SOC_maps/SOCS_0_200cm_year_2010AD_10km'}[self.dataset]

    def sld_interval(self):
        return {'Current-SOC-stocks-(0-200-cm)': '<RasterSymbolizer>' +
                                                 '<ColorMap extended="false" type="ramp">' +
                                                 '<ColorMapEntry color="#E18D67" quantity="10"  opacity="1" />' +
                                                 '<ColorMapEntry color="#CB5A3A" quantity="40"  />' +
                                                 '<ColorMapEntry color="#9D4028" quantity="80" />' +
                                                 '<ColorMapEntry color="#6D2410" quantity="160"  />' +
                                                 '<ColorMapEntry color="#380E03" quantity="400"  />' +
                                                 '</ColorMap>' + '</RasterSymbolizer>'
                }[self.dataset]
