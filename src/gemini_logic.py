import google.generativeai as genai

def check_object_with_gemini(api_key, model_name, target_img, scene_img, custom_prompt=None):
    """
    Detects if the target object exists in the scene image using Gemini.
    
    Args:
        api_key (str): Google Gemini API Key.
        model_name (str): Name of the Gemini model to use.
        target_img (PIL.Image): Image of the object to find.
        scene_img (PIL.Image): Image of the scene to search in.
        custom_prompt (str, optional): Specific instructions for the analysis.
        
    Returns:
        str: JSON string response from Gemini.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    base_prompt = """
    You are an AI assistant capable of analyzing images.
    I have provided two images:
    1. The first image is the 'Target Object' I am looking for.
    2. The second image is the 'Scene' where I want to find the object.

    Task:
    Determine if the 'Target Object' is present in the 'Scene'.
    If it is present, describe its location (e.g., on the desk, on the floor).
    """

    if custom_prompt:
        base_prompt += f"\n\n    User Instructions:\n    {custom_prompt}"

    base_prompt += """
    
    Output strictly in JSON format:
    {
        "is_present": boolean,
        "location_description": "string",
        "reasoning": "string"
    }
    """
    
    try:
        response = model.generate_content([base_prompt, target_img, scene_img])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
