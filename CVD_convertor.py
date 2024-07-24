import os
import numpy as np
from PIL import Image
from daltonlens import convert, simulate
import argparse

deficiency_dict = {
    'protan': simulate.Deficiency.PROTAN,
    'deutan': simulate.Deficiency.DEUTAN,
    'tritan': simulate.Deficiency.TRITAN,
}

simulator_dict = {
    'vienot': simulate.Simulator_Vienot1999(convert.LMSModel_sRGB_SmithPokorny75()),
    'brettel': simulate.Simulator_Brettel1997(convert.LMSModel_sRGB_SmithPokorny75()),
    'vischeck': simulate.Simulator_Vischeck(),
    'machado': simulate.Simulator_Machado2009(),
    'coblisV1': simulate.Simulator_CoblisV1(),
    'coblisV2': simulate.Simulator_CoblisV2(),
    'auto': simulate.Simulator_AutoSelect()
}

def simulate_cvd_images(sim, selected_cb_types, severity, src_list):
    for cb_type in selected_cb_types:
        print(f'Converting to {cb_type}, severity is {severity}')
        for source_dir in src_list:
            print(f'Now working on {source_dir} ...')

            target_dir = f'{source_dir}_{sim}_{cb_type}_{severity}'
            os.makedirs(target_dir, exist_ok=True)

            simulator = simulator_dict[sim]
            deficiency = deficiency_dict[cb_type]

            image_path_list = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]

            for image_name in os.listdir(source_dir)[:]:
                if image_name.endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(source_dir, image_name)
                    image = np.asarray(Image.open(image_path).convert('RGB'))

                    image_cvd = simulator.simulate_cvd(image, deficiency, severity)
                    image_cvd_pil = Image.fromarray(image_cvd)

                    target_image_path = os.path.join(target_dir, image_name)
                    image_cvd_pil.save(target_image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate color vision deficiency on images.")
    parser.add_argument('--sim', type=str, default='brettel', choices=simulator_dict.keys(), help='Simulator type.')
    parser.add_argument('--cb_types', type=str, nargs='+', default=['protan', 'deutan', 'tritan'], choices=deficiency_dict.keys(), help='Types of color blindness to simulate.')
    parser.add_argument('--severity', type=int, default=1, help='Severity of the color blindness simulation.')
    parser.add_argument('--src_list', type=str, nargs='+', default=['./data/all_resized', './data/bn_resized_label', './data/mm_resized_label'], help='List of source directories containing images.')
    args = parser.parse_args()

    simulate_cvd_images(args.sim, args.cb_types, args.severity, args.src_list)
