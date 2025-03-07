from functools import reduce
import operator
import json
import streamlit as st
import requests

paths = {
  "Type": ["myASG", "Type"],
  "VPCZoneIdentifier": ["myASG", "Properties", "VPCZoneIdentifier"],
  "Fn::GetAtt": ["myASG", "Properties", "LaunchTemplate", "Version", "Fn::GetAtt"],
  "Ref": ["myASG", "Properties", "LaunchTemplate", "LaunchTemplateId", "Ref"],
  "Version": ["myASG", "Properties", "LaunchTemplate", "Version"],
  "MaxSize": ["myASG", "Properties", "MaxSize"],
  "MinSize": ["myASG", "Properties", "MinSize"],
}

def send_to_slack():
  webhook_url = "https://hooks.slack.com/services/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"
  payload = {
    "text": f"```{json.dumps(st.session_state.json_data)}```",
  }
  headers = {'Content-Type': 'application/json'}
  response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
  if response.status_code != 200:
      raise ValueError(f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")
  else:
      print(f"Data enviada: {st.session_state.json_data}")

def get_from_dict(data, path):
  return reduce(operator.getitem, path, data)

def set_in_dict(data, path, value):
  get_from_dict(data, path[:-1])[path[-1]] = value

def find_all_keys(d, keys_list=None):
  for k, v in d.items():
      if isinstance(v, dict):
          find_all_keys(v, keys_list)
      else:
          keys_list.append(k)
  return keys_list

def display_download_button(data):
  st.download_button(
    label="Download modified JSON",
    file_name="modified_asg.json",
    mime="application/json",
    data=json.dumps(data)
  )

def display_send_to_slack_button(data):
  st.session_state.json_data = data
  st.button(
    label="Send to Slack",
    on_click=send_to_slack,
  )

st.title("Sistemas Distribuidos")
st.caption("1: Código En Python usando Streamlit que reciba un archivo en Json y lo pueda leer, mostrando el contenido.")
st.caption("3: Extraer el contenido de VPCZoneIdentifier, LaunchTemplate(Ref y Version,Fn::GetAtt), 'MaxSize'  y 'MinSize'  y Mostrarlo en pantalla: 'Contenido de ___ es:   contenido  '")
st.caption("4: Tener un dropdown para elegir “CUALQUIER” etiqueta key del JSON y una ves seleccionado poder ingresar un nuevo valor. Al final de la edición mostrar el JSON completo de nuevo.")
st.caption("5: Poder Descargar el “nuevo” Json")
st.divider()

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  bytes_data = uploaded_file.getvalue()
  json_data = json.loads(bytes_data)
  st.json(json_data)

  type = get_from_dict(json_data, paths["Type"])
  vpc_zone_identifier = get_from_dict(json_data, paths["VPCZoneIdentifier"])
  launch_template_ref = get_from_dict(json_data, paths["Ref"])
  launch_template_version = get_from_dict(json_data, paths["Version"])
  max_size = get_from_dict(json_data, paths["MaxSize"])
  min_size = get_from_dict(json_data, paths["MinSize"])

  st.header("ASG Properties")
  st.text("Contenido de Type es: " + type)
  st.text("Contenido de VPCZoneIdentifier es: " + json.dumps(vpc_zone_identifier))
  st.text("Contenido de LaunchTemplate Ref es: " + launch_template_ref)
  st.text("Contenido de LaunchTemplate Version es: " + json.dumps(launch_template_version))
  st.text("Contenido de MaxSize es: " + max_size)
  st.text("Contenido de MinSize es: " + min_size)

  st.header("Actualizar JSON")
  keys = find_all_keys(json_data, [])

  selected_option = st.selectbox("Selecciona la propiedad a modificar", keys)
  st.write("Seleccionaste: ", selected_option)

  st.text_input("Introduce el valor nuevo: ", key="new_value")
  st.write("Introdujiste: ", st.session_state.new_value)

  if st.session_state.new_value:
    st.caption("JSON modificado")
    json_data_copy = json_data.copy()
    set_in_dict(json_data_copy, paths[selected_option], st.session_state.new_value)
    st.json(json_data_copy)
    display_download_button(json_data_copy)
    display_send_to_slack_button(json_data_copy)