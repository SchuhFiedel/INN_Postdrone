using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InteractableObj : MonoBehaviour
{
    public float radius = 3f;

    void OnDrawGizmosSelected() //Callback Function by Unity
    {
        //draw graphics in the scene
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, radius);

    }
}
