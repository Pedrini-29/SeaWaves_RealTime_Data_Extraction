

#function to change the marker colour with different wave hights
def marker_color(wave):
    wave=float(wave)
    if wave > 6:
        return "black"
    elif wave > 4:
        return "red"
    elif wave > 2:
        return "orange"
    elif wave > 1:
        return "green"
    elif wave > 0.5:
        return "blue"
    else:
        return "gray"
    
def fancy_html(row, conjunto):
    
    # Access values from the row, fallback to 'N/A'
    altura_signif = row.get('Altura Signif. del Oleaje (m)', 'N/A') if isinstance(row, dict) else row.get('Altura Signif. del Oleaje (m)', 'N/A')
    altura_max = row.get('Altura Máxima del Oleaje (m)', 'N/A') if isinstance(row, dict) else row.get('Altura Máxima del Oleaje (m)', 'N/A')
    dir_media = row.get('Direcc. Media de Proced. (º)', 'N/A') if isinstance(row, dict) else row.get('Direcc. Media de Proced. (º)', 'N/A')
    dir_pico = row.get('Direcc. de pico de proced. (º)', 'N/A') if isinstance(row, dict) else row.get('Direcc. de pico de proced. (º)', 'N/A')
    periodo_medio = row.get('Periodo Medio Tm02 (s)', 'N/A') if isinstance(row, dict) else row.get('Periodo Medio Tm02 (s)', 'N/A')
    periodo_pico = row.get('Periodo de Pico (s)', 'N/A') if isinstance(row, dict) else row.get('Periodo de Pico (s)', 'N/A')
    fecha = row.get('Fecha  (GMT)', 'N/A') if isinstance(row, dict) else row.get('Fecha  (GMT)', 'N/A')
    energia = row.get('Energía del Oleaje (kJ)', 'N/A') if isinstance(row, dict) else row.get('Energía del Oleaje (kJ)', 'N/A')
    temp_mar = row.get('Temperatura del mar (°C)', 'N/A') if isinstance(row, dict) else row.get('Temperatura del mar (°C)', 'N/A')
    
    #print(altura_signif,altura_max,dir_media,dir_pico,periodo_medio,periodo_pico,fecha,energia,temp_mar)

    station = row['StationCode']
    lat = row['Latitude']
    lon = row['Longitude']

    left_col_colour = "#208AB7"
    right_col_colour = "#C5DCE7"

#html file for the markers coming from Portus REDCOS
    html_REDCOS = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station} Portus {conjunto}</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura máxima (Hmax)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_max} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. media</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{dir_media}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo de pico</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{periodo_pico} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""

    #html file for the markers coming from Portus REDEXT
    html_REDEXT = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station} Portus {conjunto}</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura máxima (Hmax)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_max} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. media</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{dir_media}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. pico</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{dir_pico}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo de pico</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{periodo_pico} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""
        #html file for the markers coming from Portus ODASMAWS
    html_ODASMAWS = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station} Portus {conjunto}</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""
#html file for the markers coming from MetOffice
    html_METOFFICE = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station} MetOffice</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Temperatura mar</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{temp_mar} °C</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitud</span></td>
<td style="width: 100px; background-color: {right_col_colour}; text-align:center;">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""
#html file for the markers coming from Labouee
    html_LABOUEE = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station} Coriolis Cotier</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<thead>
<tr>
<th style="background-color:#ffffff; text-align:left;">Parámetro</th>
<th style="background-color:#ffffff; text-align:center;">Valor</th>
</tr>
</thead>
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura máxima (Hmax)</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{altura_max} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Energía del oleaje</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{energia} kJ</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Temperatura mar</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{temp_mar} °C</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitud</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitud</span></td>
<td style="width: 100px; background-color: {right_col_colour};text-align:center;">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""
    if conjunto =="REDCOS":
        return html_REDCOS
    if conjunto =="REDEXT":
        return html_REDEXT
    if conjunto =="ODASMAWS":
        return html_ODASMAWS
    if conjunto =="METOFFICE":
        return html_METOFFICE
    if conjunto =="LABOUEE":
        return html_LABOUEE 


def c_width(conjunto):
    """function to change the width of the popup with different datasets"""
    if conjunto in {"REDCOS","REDEXT"}:
        return 330
    elif conjunto == "ODASMAWS":
        return 330
    elif conjunto == "METOFFICE":
        return 315
    elif conjunto == "LABOUEE":
        return 330

def c_height(conjunto):
    """function to change the height of the popup with different datasets"""
    if conjunto == "REDEXT":
        return 250
    elif conjunto == "REDCOS":
        return 240
    elif conjunto == "ODASMAWS":
        return 120
    elif conjunto == "METOFFICE":
        return 195
    elif conjunto == "LABOUEE":
        return 250