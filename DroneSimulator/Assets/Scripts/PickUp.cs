using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PickUp : MonoBehaviour
{
    public Transform carryPosition;
    public Camera playerCam;
    public CharacterController controller;
    public GameObject carriedObject;
    public static bool carrying = false;
    public float distance = 1;
    public float carrySmoothness = 5;

    void Update()
    {

            if (carrying && Input.GetKeyDown(KeyCode.E))
            {
                Drop();
            }
            else if (carrying)
            {
                Carry(carriedObject);
            }
            else
            {
                Pickup();
            }
    }

    void Pickup()
    {
        if (Input.GetKeyDown(KeyCode.E)) //Right Mouse button
        {
            Ray ray = new Ray(controller.transform.position, -controller.transform.up);
            RaycastHit hit;

            if(Physics.Raycast(ray, out hit, 100))
            {
                InteractableObj interactible = hit.collider.GetComponent<InteractableObj>(); // Get the Object that is hit by the ray

                if (interactible != null && interactible.canBeInteracted)
                {
                    Debug.Log("PICKUP CARRY");
                    carrying = true;
                    carriedObject = interactible.gameObject;
                }
            }
            
        }
    }
   
    void Drop()
    {
        carriedObject.GetComponent<Rigidbody>().isKinematic = false;
        carrying = false;
        carriedObject = null;
    }

    void Carry(GameObject obj)
    {
        Debug.Log("Carry");
        obj.GetComponent<Rigidbody>().isKinematic = true;
        obj.transform.position = Vector3.Lerp(obj.transform.position, carryPosition.position, carrySmoothness);
        obj.transform.rotation = Quaternion.Lerp(obj.transform.rotation, carryPosition.transform.rotation, carrySmoothness * 0.5f * Time.deltaTime);
    }

}
