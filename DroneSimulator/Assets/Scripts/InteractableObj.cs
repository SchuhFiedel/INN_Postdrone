using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InteractableObj : MonoBehaviour
{
    public float useRadius = 3f;
    public bool canBeInteracted = false;

    private void OnTriggerStay(Collider other)
    {
        GameObject obj = other.gameObject;
        if(obj.layer == LayerMask.NameToLayer("Player"))
        {
            canBeInteracted = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        GameObject obj = other.gameObject;
        if(obj.layer == LayerMask.NameToLayer("Player"))
        {
            canBeInteracted = false;
        }
    }
}
