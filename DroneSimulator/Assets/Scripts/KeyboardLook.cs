using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KeyboardLook : MonoBehaviour
{
    public float mouseSensitivity = 100f;
    private float xRotation = 0f;
    public Transform playerBody;

    // Update is called once per frame
    void Update()
    {


        if (Input.GetKey(KeyCode.Q))
        {
            xRotation = -0.1f;
        }
        else if (Input.GetKey(KeyCode.E))
        {
            xRotation = 0.1f;
        }
        else
        {
            xRotation = 0;
        }

        playerBody.Rotate(Vector3.up * xRotation);
        
    }
}
