import yaml
import re 


class ConfigurationPXGFile:
    def __init__(self, path:str):
        with open(path, encoding='utf-8') as f:
            self.text  = f.read()
        self.PADRAO = re.compile(
            r"position:\s*\n\s*y:\s*(?P<y>-?\d+)\s*\n\s*x:\s*(?P<x>-?\d+)\s*\n\s*z:\s*(?P<z>-?\d+)"
        )
        # self.BLOCO_MINIMAP = re.compile(r"^Minimap:\n(?:[ \t]+.*\n?)*", re.MULTILINE)
        self.FLAGS = re.compile(r"^  flags:[ \t]*\n(?:[ \t]{4,}.*\n?)*", re.MULTILINE)
        self.config_dict = {
            "minimap": self._get_minimap(),
            # "actions_slots": self._get_actions_slots()
        }
        

    '''
    vip list
    Minimap:
    actions-slots-info
    '''

    def _get_minimap(self):
        text = re.sub(r'(color:\s*)(#[0-9A-Fa-f]{6,8})', r'\1"\2"', self.text)
        m = self.FLAGS.search(text)
        if not m:
            raise ValueError("Bloco 'Minimap:' não encontrado no arquivo")
        
        bloco = m.group(0)
        dados = yaml.safe_load(bloco)
        marcadores = dados['flags']
        return marcadores


    # def _get_actions_slots(self):
    #     pass
    @staticmethod
    def gerar_marcador(position=None, icon="checkmark", description=None, color=None):
        linhas = ["    -"]
        # if description:
        linhas.append(f"      description: ponto novo")
        linhas += [
            "      position:",
            f"        y: {position["y"]}",
            f"        x: {position["x"]}",
            f"        z: {position["z"]}",
            f"      icon: {icon}",
        ]
        if color:
            linhas.append(f"      color: {color}")
        return "\n".join(linhas) + "\n"

    def incluir_marcadores(self, novos):
        """novos: lista de dicts com x, y, z e opcionalmente icon, description, color."""
        bloco = self.FLAGS.search(self.text).group(0)
        # existentes = set(self.config_dict["minimap"])
        # adicionar = "".join(
        #     self.gerar_marcador(**n) for n in novos
        #     if (n['x'], n['y'], n['z']) not in existentes
        # )
        # existentes = {
        #     (m['position']["x"], m['position']["y"], m['position']["z"])
        #     for m in self.config_dict["minimap"]
        # }
        # new_n = []
        # for n in novos:
        #     if (n["position"]["x"], n["position"]["y"], n["position"]["z"]) not in existentes:
        #         new_n.append(n)
        # print(new_n)
        # adicionar = "".join(
        #     self.gerar_marcador(**n) for n in novos 
        #     if (n["position"]["x"], n["position"]["y"], n["position"]["z"]) not in existentes ## atenção aqui
        # )
        # print(novos)
        adicionar = "".join(
            self.gerar_marcador(**n) for n in novos 
        )


        # if not adicionar:
        #     return self.text
        # se o bloco termina com um "-" vazio solto, insere antes dele

        m = re.search(r"    -\n?\Z", bloco)
        if m:
            novo_bloco = bloco[:m.start()] + adicionar + bloco[m.start():]
        else:
            if not bloco.endswith("\n"):
                bloco += "\n"
            novo_bloco = bloco + adicionar
        self.text = self.text.replace(bloco, novo_bloco)
        return self.text

    def export_config_file(self, path_name):
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(self.text)
