

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
    
def fancy_html(row):
    
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

    html = f"""<!DOCTYPE html>
<html>
<head>
<h4 style="margin-bottom:0; width:300px">{fecha}</h4>
<h5 style="margin-top:2px; margin-bottom:6px;">Estación: {station}</h5>
</head>
<table style="height: 100%; width: 300px; border-collapse: collapse;">
<tbody>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura significativa (Ho)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{altura_signif} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Altura máxima (Hmax)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{altura_max} m</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. media</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{dir_media}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Dir. pico</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{dir_pico}°</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo medio (Tm02)</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{periodo_medio} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Periodo de pico</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{periodo_pico} s</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Energía del oleaje</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{energia} kJ</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Temperatura mar</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{temp_mar} °C</td>
</tr>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Latitude</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{lat}</td>
<tr>
<td style="background-color: {left_col_colour};"><span style="color: #ffffff;">Longitude</span></td>
<td style="width: 100px; background-color: {right_col_colour};">{lon}</td>
</tr>
</tr>
</tbody>
</table>
</html>
"""

    return html